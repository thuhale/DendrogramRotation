import io
import sys
from TreeNode import TreeNode
from PrintCluster import PrintCluster

Rotate_ratio_const = 2.0

def rotateRight(root, pivot):
    rootCount = root.Count
    root.Count = rootCount - pivot.Count + pivot.right.Count
    pivot.Count = rootCount
    root.left = pivot.right
    pivot.right = root
    return pivot


def rotateLeft(root, pivot):
    rootCount = root.Count
    root.Count = rootCount - pivot.Count + pivot.left.Count
    pivot.Count = rootCount
    root.right = pivot.left
    pivot.left = root
    return pivot

# Split off pivot.right's right node and move it over to the root.right branch
def splitSubRight(root):
    if root.Count == 6:
        debugHere = True

    pivot = root.left
    moveNode = pivot.right.right
    leftNode = pivot.right.left
    newInterNode = TreeNode(0)
    newInterNode.right = root.right
    newInterNode.left = moveNode
    newInterNode.Count = newInterNode.left.Count + newInterNode.right.Count

    pivot.right = None
    pivot.right = leftNode
    pivot.Count = pivot.left.Count + pivot.right.Count
    root.right = newInterNode
    return root

# Split off pivot.right's right node and move it over to the root.right branch
def splitSubLeft(root):
    pivot = root.right
    moveNode = pivot.left.left
    rightNode = pivot.left.right
    newInterNode = TreeNode(0)
    newInterNode.left = root.left
    newInterNode.right = moveNode
    newInterNode.Count = newInterNode.left.Count + newInterNode.right.Count

    pivot.left = None
    pivot.left = rightNode
    pivot.Count = pivot.left.Count + pivot.right.Count
    root.left = newInterNode
    return root


def checkAndRotate(root):
    queue = [(root, None, '')]  #Tuple of (TreeNode, parent, parent's direction L or R)
    index = 0

    while index < len(queue):
        curNode = queue[index][0]
        canRight, simple = canRightRotate(curNode)

        if canRight:
            if simple:
                temp = rotateRight(curNode, curNode.left)
                queue.append((temp.right, temp, 'R'))
                parent = queue[index][1]
                if parent is not None:
                    if queue[index][2] == 'L':
                        parent.left = temp
                    else:
                        parent.right = temp
            else:  # pivot-split right operation
                temp = splitSubRight(curNode)
                queue.append((temp.left, temp, 'L'))
                queue.append((temp.right, temp, 'R'))
            queue[index] = (temp, queue[index][1], queue[index][2])
        else:
            canLeft, simple = canLeftRotate(curNode)
            if canLeft:
                if simple:
                    temp = rotateLeft(curNode, curNode.right)
                    queue.append((temp.left, temp, 'L'))
                    parent = queue[index][1]
                    if parent is not None:
                        if queue[index][2] == 'L':
                            parent.left = temp
                        else:
                            parent.right = temp
                else:   # pivot-split left operation
                    temp = splitSubLeft(curNode)
                    queue.append((temp.left, temp, 'L'))
                    queue.append((temp.right, temp, 'R'))
                queue[index] = (temp, queue[index][1], queue[index][2])

        index += 1
        # if index > 128: break

    return queue[0][0]

# Can rotate right? If yes, simple rotate or right pivot-split-substitue?
def canRightRotate(root):
    pivot = root.left
    if (pivot.right is None) or (pivot.Count < Rotate_ratio_const * root.right.Count):
        return False, False

    if (pivot.right.left is None) or (pivot.right.right is None):
        simpleRotate = True
    else:
        rightCount = root.right.Count + pivot.right.Count
        simpleRatio = 1.0 * pivot.left.Count / rightCount

        if simpleRatio < 1:
            simpleRatio = 1 / simpleRatio

        leftCount = pivot.left.Count + pivot.right.left.Count
        rightCount = root.right.Count + pivot.right.right.Count
        splitRatio = 1.0 * leftCount / rightCount
        if splitRatio == 0:
            debugHere = True

        if splitRatio < 1:
            splitRatio = 1 / splitRatio

        if simpleRatio <= splitRatio:  #simple rotate produces more balanced result
            simpleRotate = True
        else:
            simpleRotate = False

    return True, simpleRotate


# Can rotate left? If yes, simple rotate or left pivot-split-substitue?
def canLeftRotate(root):
    pivot = root.right
    if (pivot.left is None) or (pivot.Count < Rotate_ratio_const * root.left.Count):
        return False, False

    if (pivot.left.left is None) or (pivot.left.right is None):
        simpleRotate = True
    else:
        leftCount = root.left.Count + pivot.left.Count
        simpleRatio = 1.0 * pivot.right.Count / leftCount
        if simpleRatio < 1:
            simpleRatio = 1 / simpleRatio

        rightCount = pivot.right.Count + pivot.left.right.Count
        leftCount = root.left.Count + pivot.left.left.Count
        splitRatio = 1.0 * leftCount / rightCount
        if splitRatio < 1:
            splitRatio = 1 / splitRatio

        if simpleRatio <= splitRatio:  #simple rotate produces more balanced result
            simpleRotate = True
        else:
            simpleRotate = False

    return True, simpleRotate


def setWeightedTest(index,leftNode, rightNode):
    if index == 1:
        leftNode.Count = 20
        rightNode.Count = 20
    elif index == 2:
        leftNode.Count = 28
        rightNode.Count = 32
    elif index == 4:
        leftNode.Count = 10
        rightNode.Count = 20


def getLeftmostNode(curNode):
    node = curNode
    while node.left is not None:
        node = node.left
    return node

def prepareTree(orderDict):
    filePath = 'input/pcp_merge.csv'
    file = open(filePath, 'r')
    file.readline()
    steps = []
    steps.append(TreeNode(-1))

    for lineStr in file:
        pieces = lineStr.replace('"', '')[:-1].split(',')
        source = int(pieces[0])
        target = int(pieces[1])
        if source < 0:  #source is a nodeIndex
            leftNode = TreeNode(abs(source))
        else:
            leftNode = steps[source]

        if target < 0:
            rightNode = TreeNode(abs(target))
        else:
            rightNode = steps[target]

        newRoot = TreeNode(0)
        newRoot.Count = leftNode.Count + rightNode.Count
        newRoot.left = leftNode
        newRoot.right = rightNode

        leftOrder = orderDict[getLeftmostNode(leftNode).Value]
        rightOrder = orderDict[getLeftmostNode(rightNode).Value]
        if leftOrder > rightOrder:
            newRoot.left, newRoot.right = newRoot.right, newRoot.left

        newRoot = checkAndRotate(newRoot)
        steps.append(newRoot)

    file.close()
    return newRoot

def readOrderFile(filePath):
    file = open(filePath, 'r')
    file.readline()
    orderDict = {}

    for lineStr in file:
        pieces = lineStr.replace('"', '')[:-1].split(',')
        index = int(pieces[2])
        orderDict[index] = int(pieces[3])

    file.close()
    return orderDict

orderDict = readOrderFile('input/pcp_sorted_order.csv')
lastRoot = prepareTree(orderDict)
print 'Total nodes: ' + str(lastRoot.Count)
print 'Left:' + str(lastRoot.left.Count) + '  , Right:' + str(lastRoot.right.Count)
clusterObj = PrintCluster('output/pcp_label_64.csv')
clusterObj.produceClusters(lastRoot, 64)
