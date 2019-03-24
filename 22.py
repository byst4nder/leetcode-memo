"""
给n对括号，输出所有可能的、合法的排列。

.. 找了一堆教程还是没看懂……

一开始觉得有点决策树的感觉，第一个字符串可以选择放 ``(`` 或者 ``)`` ，第二个字符串可以选择放 ``(`` 或者 ``)`` ……每一个选择都形成了一个分支，形成了一个二叉树。

看了一个 视频_ ，讲的很好。所谓backtracking回溯，就是用深度优先方式遍历决策树，并且在遍历的某些时候，不用下到最后一层就能提前知道需不需要继续深入。比如根节点的右边子节点是 ``)`` ，显然不能在出现左括号之前就出现右括号，所以从这个右边子节点开始的右边子树整个都不用遍历了，直接扔掉，因为无论怎么遍历，结果都是错的。

从组合的角度来看，回溯可以帮助缩减状态空间，从而降低时间复杂度，但是至于能降低多少、是仅仅降低前面的常数、还是降低阶数，取决于具体的问题里能否在未完全产生解、或者说产生了部分解之后能否直接判断完整解是否正确。

.. _视频: https://www.youtube.com/watch?v=sz1qaKt0KGQ

回到这道题上来，在每个节点，我们都有两个选择

-   接下来放 ``(`` （作为左边节点）
-   或者接下来放 ``)`` （作为右边节点）

但是同时受到一些限制

-   从根节点到任何一个节点的路径上 [#]_ ，左括号数量总数不能超过n
-   从根节点到任何一个节点的路径上，右括号数量总数不能超过n
-   从根节点到任何一个节点的路径上，右括号数量总数不能超过左括号数量总数

    这个条件很关键，因为不能在还没有放左括号的时候就先放右括号，比如 ``), ())`` 之类的都不可以。

.. [#] 这里我强调了 **从根节点到任何一个节点的路径上** ，一旦在遍历过程中到达某个节点时，发现上面的限制没有满足，就可以直接认为从这个节点开始的子树是空树，无需再遍历下去了。

现在我们可以粗略地画出这个决策树了，以n = 2为例，整个决策树是这样的

::

    [""]
    ["(", null]
    ["(", ")", null, null]
    [null, ")", null, ")", null, null, null, null]

在根节点处，不考虑限制可以选择放 ``(`` 或者 ``)``。如果选择了第一个放 ``(`` ，那么第二个位置还可以选择放 ``(`` 或者 ``)`` ；但是如果选择了第一个放 ``)`` ，第三个限制 **右括号数量总数不能超过左括号数量总数** 无法满足，所以整个右边子树不存在。

如果第二个位置选择放 ``(`` ，那么第三个位置不考虑限制可以放 ``(`` 或者 ``)`` ，但是考虑了限制后，会发现如果放 ``(`` ，那么到这里的路径变成了 ``(((``` ，有三个左括号，会违反 **左括号数量总数不能超过n** 的限制；如果放 ``)`` ，不违反任何限制。

大概就是这样一个思路，最终的结果是输出决策树中根节点到每个叶子的路径。在遍历过程中一旦遇到当前节点不符合限制的，直接返回空路径就可以了。

还有一个问题是，以往的树的操作都是先给你一个现成的树让你遍历，而这里是需要你一边产生树一边判断，有点区别。在设计递归函数的时候，可以反过来设计，不要用左括号、右括号的数量，可以变成可用的左括号、右括号的数量，这样当比如说左括号可用的数量到0的时候，就直接知道不能再加任何左括号了，否则会不满足限制，接下去也只有一条路径了，可以直接返回剩下的所有右括号，提高效率。

.. 或者说这道题里其实没有非常明显的树，只是我们自己的幻想。
"""

from typing import *

class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        return self.preorderTraversal(n, n)

    def preorderTraversal(self, left: int, right: int) -> List[str]: # left是这个节点和接下去允许放的左括号的数量，right同理
        if left == 0 and right > 0: # 左括号可用数量为0，不能再添加左括号了，右括号可用数量还有，所以继续下去也只剩下一条路径走到底了，也就是只能添加右括号了，所以直接返回剩下的这条路径。
            return [")" * right]
        elif 0 <= left and left <= right: # 满足限制的其他情况
            return [
                "(" + v for v in self.preorderTraversal(left - 1, right) # 左边子树继续走下去的所有路径
            ] + [
                ")" + v for v in self.preorderTraversal(left, right - 1) # 右边子树继续走下去的所有路径
            ]
        else: # 其他的情况，比如left < 0等等
            return [] # 统统返回空路径

s = Solution()
print(s.generateParenthesis(3))