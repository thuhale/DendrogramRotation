class TreeNode:
    left = None
    right = None
    parent = None
    upLink = None

    Value = ''
    Count = 0  # count how many nodes under and including itself.

    def __init__(self, nodeIndex):
        self.Count = 1
        self.Value = nodeIndex
        self.parent = None


class TreeOp:
    @staticmethod
    def getRatio(nodeA, nodeB):
        ratio = 1.0 * nodeA.Count / nodeB.Count
        if ratio < 1:
            ratio = 1 / ratio
        return ratio

    @staticmethod
    def correctRatio(num1, num2):
        ratio = 1.0 * num1 / num2
        if ratio < 1:
            ratio = 1 / ratio
        return ratio

    # Determine if current node is on the Left, or Right branch of root node
    @staticmethod
    def getOrientation(curNode, root):
        node = curNode
        while node.parent is not None:
            if node.parent == root:
                if root.left == node:
                    return 'L'
                else:
                    return 'R'
            node = node.parent
        return ' '

    @staticmethod
    def rotateRight(root, pivot):
        rootCount = root.Count
        root.Count = rootCount - pivot.Count + pivot.right.Count
        pivot.Count = rootCount
        root.left = pivot.right
        root.left.parent = root

        temp = root.upLink
        root.upLink = pivot.right.upLink
        pivot.right.upLink = pivot.upLink
        pivot.upLink = temp

        pivot.right = root
        pivot.parent = root.parent
        root.parent = pivot
        return pivot  # new root

    # Split off pivot.right's right node and move it over to the root.right branch
    @staticmethod
    def splitSubRight(root):
        pivot = root.left
        moveNode = pivot.right.right
        leftNode = pivot.right.left

        newInterNode = TreeNode(0)
        newInterNode.upLink = moveNode.upLink
        newInterNode.right = root.right
        root.right = newInterNode
        moveNode.upLink = pivot.upLink

        newInterNode.left = moveNode
        moveNode.parent = newInterNode
        newInterNode.Count = newInterNode.left.Count + newInterNode.right.Count

        pivot.upLink = leftNode.upLink
        leftNode.upLink = pivot.right.upLink
        pivot.right = leftNode
        leftNode.parent = pivot

        pivot.Count = pivot.left.Count + pivot.right.Count
        root.right = newInterNode
        newInterNode.parent = root
        return root
