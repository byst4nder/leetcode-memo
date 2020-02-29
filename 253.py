"""
给一些左闭右开区间，代表会议的起止时间，最少需要多少间会议室？

说是用greedy，但是我不能证明为什么可以用greedy。

做法是这样的，先把所有的会议按起始时间从小到大排序，然后对于每个会议，都去找一间这样的屋子

-   上一个会议结束时间和这个会议不冲突
-   上一个会议结束时间尽可能早

如果能找到这样的屋子，就把当前会议放在这个屋子里举办。

如果找不到这样的屋子，就要新开一间屋子，来开当前这个会议。

那么为什么是从所有不冲突的屋子里、找那间结束时间最早的屋子来举办当前会议、而不是找那间结束时间最晚的屋子来举办当前会议呢？我的粗略理解是，有点像pinterest的那个瀑布流，每次有新的图片上来，都是放在最后一张图片最靠上的那一列的最下面，而不会放在最后一张图片最靠下的那一列，这样视觉上会觉得，虽然是瀑布流，但是却显得很平均。

我怀疑这里也是一样的道理。如果你把当前会议放在结束时间最晚的那个屋子里举办的话，那么结束时间最早的那个屋子就会空着，而且更糟糕的是，因为我们一开始按起始时间排序了，当前会议之后的那个会议的开始时间比当前会议还要晚。这样就会导致某些屋子很满、但是某些屋子很空。

证明我需要想一想。
"""

from typing import *

import heapq

class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        intervals = sorted(intervals, key=lambda v: v[0]) # 先把所有的会议按起始时间从小到大排序
        roomFinishingTimes = [] # 记录每一间会议室里最近一次会议的结束时间
        heapq.heapify(roomFinishingTimes) # 因为每次都需要找一间最近一次会议结束时间最早的屋子，所以用heap就可以很快

        for v in intervals: # 对于每个会议
            if roomFinishingTimes != []: # 有会议已经在举行了
                if roomFinishingTimes[0] <= v[0]: # 看上一次会议结束时间的最早的那个屋子里的那次会议的结束时间，如果不冲突
                    heapq.heappop(roomFinishingTimes) # 就把当前会议放在这个屋子里举行
                    heapq.heappush(roomFinishingTimes, v[1])
                else: # 如果冲突，那么说明所有的屋子里的正在举办的会议都和当前会议时间上有冲突。因为这个屋子里的会议已经是结束的最早的了，结束的最早的会议都和当前会议冲突，那么结束的晚的会议一定和当前会议冲突
                    heapq.heappush(roomFinishingTimes, v[1]) # 只能开一间新的屋子举办当前会议
            else: # 所有的屋子都是空的、还没有会议在举行
                heapq.heappush(roomFinishingTimes, v[1]) # 那当然随便选一间屋子都行

        return len(roomFinishingTimes)

s = Solution()
print(s.minMeetingRooms([[0, 30],[5, 10],[15, 20]])) # 2
print(s.minMeetingRooms([[7,10],[2,4]])) # 1
print(s.minMeetingRooms([[2,15],[36,45],[9,29],[16,23],[4,9]])) # 2
print(s.minMeetingRooms([[64738,614406],[211748,780229],[208641,307338],[499908,869489],[218907,889449],[177201,481150],[123679,384415],[120440,404695],[191810,491295],[800783,826206],[165175,221995],[420412,799259],[484168,617671],[746410,886281],[765198,792311],[493853,971285],[194579,313372],[119757,766274],[101315,917883],[557309,599256],[167729,723580],[731216,988021],[225883,752657],[588461,854166],[231328,285640],[772811,869625],[892212,973218],[143535,306402],[336799,998119],[65892,767719],[380440,518918],[321447,558462],[54489,234291],[43934,44986],[11260,968186],[248987,707178],[355162,798511],[661962,781083],[149228,412762],[71084,953153],[44890,655659],[708781,956341],[251847,707658],[650743,932826],[561965,814428],[697026,932724],[583473,919161],[463638,951519],[769086,785893],[17912,923570],[423089,653531],[317269,395886],[412117,701471],[465312,520002],[168739,770178],[624091,814316],[143729,249836],[699196,879379],[585322,989087],[501009,949840],[424092,580498],[282845,345477],[453883,926476],[392148,878695],[471772,771547],[339375,590100],[110499,619323],[8713,291093],[268241,283247],[160815,621452],[168922,810532],[355051,377247],[10461,488835],[220598,261326],[403537,438947],[221492,640708],[114702,926457],[166567,477230],[856127,882961],[218411,256327],[184364,909088],[130802,828793],[312028,811716],[294638,839683],[269329,343517],[167968,391811],[25351,369583],[210660,454598],[166834,576380],[296440,873280],[660142,822072],[33441,778393],[456500,955635],[59220,954158],[306295,429913],[110402,448322],[44523,88192],[231386,353197],[120940,902781],[348758,597599],[329467,664450],[208411,890114],[230238,516885],[434113,602358],[349759,419831],[10689,308144],[94526,180723],[435280,986655],[611999,690154],[75208,395348],[403243,489260],[498884,611075],[487209,863242],[13900,873774],[656706,782943],[53478,586952],[226216,723114],[554799,922759],[467777,689913],[80630,147482],[277803,506346],[532240,976029],[206622,761192],[148277,985819],[10879,807349],[952227,971268],[172074,919866],[239230,384499],[607687,984661],[4405,264532],[41071,437502],[432603,661142],[144398,907360],[139605,360037],[943191,997317],[12894,171584],[382477,800157],[452077,518175],[208007,398880],[375250,489928],[384503,726837],[278181,628759],[114470,635575],[382297,733713],[156559,874172],[507016,815520],[164461,532215],[17332,536971],[418721,911117],[11497,14032]])) # 77