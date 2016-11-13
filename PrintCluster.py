from TreeNode import TreeNode

class PrintCluster:
    def __init__(self, path):
        self.filePath = path

    def printClusters(self, clusterRoots):
        file = open(self.filePath, 'w+')
        dict = {}
        number = 1
        for cluster in clusterRoots:
            root = cluster[0]
            queue = [root]
            results = []
            index = 0
            while index < len(queue):
                node = queue[index]
                if node.Value > 0:
                    results.append(str(node.Value))
                    dict[node.Value] = number
                if node.left is not None and (str(node.left.Value) not in dict):
                    queue.append(node.left)
                if node.right is not None and (str(node.right.Value) not in dict):
                    queue.append(node.right)
                index += 1

            number += 1

        nodeList = sorted(dict.keys())
        for node in nodeList:
            file.write(str(node) + ',' + str(dict[node]) + '\n')
        file.close()


    def produceClusters(self, root, clusterNr):
        level = 0
        clusterRoots = []
        clCount = 0
        queue = [(root, 1)]
        curIndex = 0

        while clCount < clusterNr:
            level += 1
            index = curIndex
            while index < len(queue):
                if queue[index][1] > level:
                    break
                node = queue[index][0]
                if node.left is not None:
                    queue.append((node.left, level+1))
                if node.right is not None:
                    queue.append((node.right, level+1))
                index += 1

            clCount = index - curIndex
            if clCount >= clusterNr:
                clusterRoots = queue[curIndex:index]
            curIndex = index

        print 'Required number of levels: ' + str(level)
        self.printClusters(clusterRoots)
