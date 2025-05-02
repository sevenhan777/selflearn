def choose_firstn(take, num_reps, failure_domain, chooseleaf, pgid):
    result, osd_result = empty_list
    for rep in range(num_reps):
        in_bucket = take  # start item
        trial = rep
        while trial < MAX_TRIES + rep:
            item = bucket_choose(in_bucket, pgid, trial)                  //pgid 对于同一个数据是不变的，因此需要调整bucket id 和重试次数这两个参数，来应对选到不合适osd的情况
            if item.type != failure_domain:  # go deeper
                in_bucket = item
                continue
            if item in result:  # collide, pick again
                trial += 1
                continue
            if failure_domain == OSD:
                if is_out(item):  # check reweight value of item(OSD)      //过载测试 手动调整reweight reweight越大越容易被选中
                    trial += 1
                    continue
            elif chooseleaf:
                osd = choose_firstn(item, 1, OSD, False, pgid)
                if osd:  # OK, found a valid osd
                    result.append(item)
                    osd_result.extend(osd)
                    break
                else:  # failed to find an available osd
                    trial += 1
                    continue
            else:
                result.append(item)  # OK, found a valid one
                break
                
    if chooseleaf:
        result = osd_result
