class Node:
    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.feature_index = 0
        self.threshold = 0
        self.left = None
        self.right = None

class MyDecisionTreeClassifier:
    def __init__(self, max_depth):
        self.max_depth = max_depth
    
    def gini(self, groups, classes):
        total = len(groups[0]) + len(groups[-1])
        gini = 0
        for group in groups:
            if len(group) == 0:
                continue
            sigma = 0
            for class_val in classes:
                probability = ([row[-1] for row in group].count(class_val) / len(group))**2
                sigma += probability
            gini += (1 - sigma) * len(group)/total
        return gini
    
    def split_data(self, X, y) -> tuple[int, int]:
        listed_Xy = [list(X[i]) + [y[i]] for i in range(len(X))]
        classes = list(set(row[-1] for row in listed_Xy))
        b_index, b_value, b_score = 999, 999, 999
        for column in range(len(listed_Xy[0]) - 1):
            for row in listed_Xy:
                groups = self.create_groups(row[column] ,column, listed_Xy)
                gini_val = self.gini(groups, classes)
                if gini_val < b_score:
                    b_index, b_value, b_score = column, row[column], gini_val
        return (b_index, b_value, groups)
    
    def create_groups(self, thr, idx, listed_Xy):
        left, right = [], []
        for xy in listed_Xy:
            if xy[idx] <= thr:
                left.append(xy)
            else:
                right.append(xy)
        return (left, right)

    def to_terminal(self,group):
        outcomes = [row[-1] for row in group]
        return max(set(outcomes), key=outcomes.count)

    def fit(self, X, y):
        self.tree = self.build_tree(X, y)
        return self.tree

    def build_tree(self, X, y, depth = 0):
        
        node = Node(X, y)
        splitted = self.split_data(X, y)
        node.feature_index = splitted[0]
        node.threshold = splitted[1]
        
        left = [(i[node.feature_index] <= node.threshold) for i in X]
        leftX, lefty = X[left], y[left]
        leftXy = [list(leftX[i]) + [lefty[i]] for i in range(len(leftX))]
        right = [(i[node.feature_index] > node.threshold) for i in X]
        rightX, righty = X[right], y[right]
        rightXy = [list(rightX[i]) + [righty[i]] for i in range(len(rightX))]
         
        if len(rightXy) == 0 or len(leftXy) == 0:
            node.left = node.right = self.to_terminal(leftXy + rightXy)
            return
        
        if depth >= self.max_depth:
            node.left, node.right = self.to_terminal(leftXy), self.to_terminal(rightXy)
            return

        if len(set(lefty)) == 1:
            node.left = self.to_terminal(leftXy)
        else:
            node.left = self.build_tree(leftX, lefty, depth + 1)
        
        if len(set(righty)) == 1:
            node.right = self.to_terminal(rightXy)
        else:
            node.right = self.build_tree(rightX, righty, depth + 1)

        return node

    def predict(self, X):
        return [self._predict(self.tree, inputs) for inputs in X]

    def _predict(self, node, X_test):
        if X_test[node.feature_index] < node.threshold:
            if isinstance(node.left, Node):
                return self._predict(node.left, X_test)
            else:
                return node.left
        else:
            if isinstance(node.right, Node):
                return self._predict(node.right, X_test)
            else:
                return node.right
