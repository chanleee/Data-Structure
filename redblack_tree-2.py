class RedBlackTree():
    # Node class - DO NOT MODIFY
    class _Node:
        RED = object()
        BLACK = object()
        """Lightweight, nonpublic class for storing a node."""
        __slots__ = '_element', '_parent', '_left', '_right', '_color' # streamline memory usage

        def __init__(self, element, parent=None, left=None, right=None, color=RED):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right
            self._color = color

    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = None
        self._size = 0

    def __len__(self):
        return self._size

    # Search for the element in the red-black tree.
    # return: _Node object, or None if it's non-existing
    
    """
    search(self,element)는 root가 none인 경우, 즉 tree가 비어있는 경우에 None을 리턴하고 그 외의 경우에는 self._search_sub에 element를 넘겨 해당 함수를 실행시키는 함수이다.
    
    :param element: 찾고자하는 element를 의미한다.
    :return: 찾고자 하는 element를 가진 노드의 element를 리턴하거나 찾지 못한 경우 None을 리턴하게 된다.
    """
    def search(self, element):
        if self._root == None:
            return None
        else:
            return self._search_sub(self._root, element)
    
    """
    _search_sub(self,node,element)는 search(self,element)에서 호출되어 각 노드간의 element를 비교하며 root에서 element를 찾을때까지 재귀적으로 호출되고 만약 찾으면 그 노드의 element를 return, 찾지 못하면 None을 리턴한다.
    
    :param node: 이 노드는 검색 시점에 있는 노드이며 이 노드의 element와 찾고자 하는 element와의 비교를 통해 찾고자 하는 노드를 찾아간다.
    :return: node를 찾으면 node._element를 return, 찾지 못하면 None을 return
    """
    def _search_sub(self, node, element):
        if node._element == element:
            return node._element
        elif node._element < element:
            if node._right == None:
                return None
            else:
                return self._search_sub(node._right, element)
        elif node._element > element:
            if node._left == None:
                return None
            else:
                return self._search_sub(node._left, element)
    
    """
    insert(self, element)는 우선 root가 없는, 즉 트리에 아무 노드도 없을때 insert를 해주는 경우와 그렇지 않을때 insert를 해주는 경우로 나눈다. 첫 경우에서는, insert하고자 하는 element를 가지는 node를 만들어주고 나서 해당 노드를 루트 노드로 지정하고 self._size에 1을 더해준다. 두번째 경우에서는 insert하고자 하는 element를 가지는 노드를 만들어주고 나서 노드가 들어가야할 위치를 찾고 노드를 insert해주는 self._search_n_add_for_insert를 호출하고 그 뒤에 double red 상황이 발생할시 이를 self._process_double_red를 호출하여 해결해주고 self._size를 1 더해준다.
    추가적으로, 이 insert function의 경우 자료구조 강의에서의 설명에 따라 넣어주는 위치가 root인 경우에는 black node를 넣어주고 그 외의 경우에는 red node를 넣어주게 된다.
    
    :param element: 트리에 insert 해주고자 하는 element를 의미한다.
    """
    def insert(self, element):
        if self._root == None:
            sub1 = self._Node(element, color=self._Node.BLACK)
            self._root = sub1
            self._size +=1
            
        else:
            sub2 = self._Node(element, color=self._Node.RED)
            self._search_n_add_for_insert(sub2) # 뭔가 추가적인 서술이 필요할 것 같긴 해
            if sub2._parent._color == self._Node.RED and sub2._color == self._Node.RED:
                self._process_double_red(sub2)
            self._size +=1
                
    """
    _search_n_add_for_insert(self, node)의 경우에는 해당하는 노드가 들어가야할 위치를 찾아주고 그 위치에 노드를 넣어주는 기능을 하는 함수로, 먼저 search 부분부터 설명하자면, search_point는 위에서 진행하였던 search에서처럼 처음에 self._root로 잡아주고 tmp_parent라는 변수를 만들게 된다. 이 변수를 만드는 이유는 위에서 진행했던 search처럼만 진행하게 된다면 넣어줄 위치를 찾게 되는 것이라 결국 없는 노드에 대한 search가 이루어지게 되어서 None이 리턴될 것이기 때문에 넣어주기 직전의 위치를 찾는다고 생각하면 쉽다. 그래서 처음에는 tmp_parent의 초기값을 None으로 설정해주고 while문과 그 안의 내용이 돌아가면서 tmp_parent를 node._element가 들어가야할 노드의 직전 노드로 업데이트 해준다. while문 뒤에 node._parent를 tmp_parent로 업데이트 해주고 이 node._parent의 element와 넣고자 하는 element와의 비교를 통해 node._parent의 왼쪽과 오른쪽 중 어디에 들어가야 할지를 알아낸 뒤에 그 자리에 node를 넣어준다. (node._parent의 child로 연결시켜준다.)
    
    :param node: insert 하고자하는 노드를 의미한다.
    """
    def _search_n_add_for_insert(self, node):
        search_point = self._root
        tmp_parent = None
        while search_point:
            tmp_parent = search_point
            if search_point._element > node._element:
                search_point = search_point._left
            else:
                search_point = search_point._right
        node._parent = tmp_parent
        if node._parent._element < node._element:
            node._parent._right = node
        else:
            node._parent._left = node

    """
    _process_double_red의 경우 node를 넣음으로써 발생한 double red 상황을 처리하기 위한 함수로 parent의 형제 노드의 색상에 따라서 경우의 수가 우선 나뉜다. 부모의 형제 노드의 색상이 black인 경우(none인 경우를 포함) 단지 구조가 맞지 않는 케이스인 것이기 때문에 reconstruct를 하는 작업이 요구된다. 이때, node._parent와 node._parent._parent간의 연결 관계, node와 node._parent간의 연결 관계, 즉 왼쪽 자식인지 오른쪽 자식인지에 따라 경우의 수가 나뉘고 그 경우에 따라 reconstruct 하기 전 색상을 바꾸어 주어야 하는 위치가 달라지게 된다. node._parent와 node._parent._parent간의 연결 관계가 node와 node._parent간의 연결 관계에서도 유지되는 경우(right-right, left-left)에는 node color는 red, parent color는 black, parent의 parent 컬러는 red로 바꾸어주고 reconstruct를 진행해주게 되고, 그 연결관계가 유지되지 않는 경우(right-left, left-right)에는 node color는 black, node parent color는 red, node parent의 parent color는 red로 하여서 reconstruct를 진행해주게 된다. 만약 부모의 형제 노드의 색상이 red인 경우는 overflow에 해당하는 경우로 split에 해당하는 recoloring 작업이 이루어져야 한다. 따라서 self._recoloring_for_insert를 해주고 이에 따라 node의 parent의 parent가 red가 되었을텐데 node의 parent의 parent의 parent가 다시 red의 경우 다시 double red의 상황이므로 다시 self._process_double_red를 node의 parent의 parent 자리에서 진행한다. 여기서 node._parent._parent._parent가 None인 경우 그 색깔이 없어서 오류가 나올수도 있으므로 그 이전에 node._parent._parent._parent가 None인지 아닌지를 확인해준다.
    
    :param node: double red가 발생한 위치의 노드를 이야기한다. (double red 노드 둘 중 아래에 위치하게 되는 노드)
    """
    def _process_double_red(self, node):
        if self._sibiling(node._parent) == None or self._sibiling(node._parent)._color == self._Node.BLACK:
            if node._parent._right == node and node._parent._parent._right == node._parent:
                node._color = self._Node.RED
                node._parent._color = self._Node.BLACK
                node._parent._parent._color = self._Node.RED
                self._reconstruct(node)
                
            elif node._parent._left == node and node._parent._parent._left == node._parent:
                node._color = self._Node.RED
                node._parent._color = self._Node.BLACK
                node._parent._parent._color = self._Node.RED
                self._reconstruct(node)
                
            elif node._parent._right == node and node._parent._parent._left == node._parent:
                node._color = self._Node.BLACK
                node._parent._color = self._Node.RED
                node._parent._parent._color = self._Node.RED
                self._reconstruct(node)
                
            elif node._parent._left == node and node._parent._parent._right == node._parent:
                node._color = self._Node.BLACK
                node._parent._color = self._Node.RED
                node._parent._parent._color = self._Node.RED
                self._reconstruct(node)
            
        elif self._sibiling(node._parent)._color == self._Node.RED:
            self._recoloring_for_insert(node)
            if node._parent._parent._parent != None:
                if node._parent._parent._parent._color == self._Node.RED:
                    self._process_double_red(node._parent._parent)
        
    """
    delete(self, element)는 element에 해당하는 노드를 트리에서 끊어주는 기능을 하는 함수이다. 즉, 트리에서 해당 element를 remove한다. 그 기능을 수행하기 위해서, 먼저 self._search_for_delete(element)를 통해 지우고자 하는 target 노드를 잡아준다. 여기서 새로운 search를 또 구현한 이유는 이전 search는 element를 return 했기 때문이다. 그리고 나서 지워진 element를 리턴하는 기능도 구현해야되기 때문에 A 변수에 target 노드의 element를 담아주고 지워주는 기능을 모두 수행한 뒤에 이를 return 한다.
    본격적으로 지워지는 기능 수행 과정을 보면, 먼저 지워지는 노드의 자식이 모두 없는 경우(case1), 자식이 모두 있는 경우(case2), 한쪽 자식만 있는 경우(case3)로 나뉘게 된다.
    
    case1: target 노드의 자식이 모두 없는 경우에서 target 노드가 루트인 경우에는 target의 element는 None으로 바꾸어주고 self._root도 None으로 바꾸어준다. 그리고 self._size를 1 빼준다. target의 color가 black인 경우에는 먼저 target 노드를 지우기 전에 self._process_double_black을 호출하여 target이 지워진 이후 상황에서 발생하는 double black을 처리해주고 그 뒤에 target이 parent의 왼쪽인지 오른쪽인지에 따라 케이스를 나누고 parent의 child자리에서 제외시킨다.(None 처리) 그 뒤에 self._size를 1 빼준다. 만약 target의 color가 red인 경우에는 앞선 경우에서 self_process_double black을 하는 단계를 제외한 나머지 단계를 진행해주면 된다.
    
    case2: 이 경우에는 일단 target을 바로 지우는 것이 아니라 target의 successor와 element을 서로 교환한 뒤 target의 successor 자리에서 delete 작업이 이루어진다고 생각하면 된다. 이 작업을 수행하기 위해서 우선 target의 successor의 color가 블랙인지 아닌지에 따라 경우를 나눈다.
    target의 successor의 색상이 블랙인 경우는 다음과 같이 처리한다.
    -> target의 successor가 그 부모의 왼쪽인지 오른쪽인지에 따라 경우를 나누는데 오른쪽인 경우 target의 successor의 왼쪽 자식이 없다고 생각하면 되고 target의 오른쪽 자식이 있는지 없는지에 따라 다시 경우를 나누게 되고 오른쪽 자식이 없다면 둘의 element를 바꾸고 이제 지우는 노드가 target의 successor가 되었으므로 target에 self._successor(target)을 지정하고 target에서(원래 successor 자리에서) double black을 처리해준다. 처리가 끝나면 그 부모의 왼쪽 자식인지 오른쪽 자식인지 구분한 뒤 그 쪽 자식을 None 처리를 해주고 self._size를 1빼준다. 만약, 오른쪽 자식이 있는 경우라면 element를 교환하고 target에 self._successor(target)을 지정해주고 나서 target의 오른쪽 자식과 target의 부모를 자식 부모 관계로 연결해주는 과정이 필요하다. 그래서 이 과정을 거치고 나서 target._parent._right(원래는 target._right 노드에 해당하고 자리 자체는 target에 해당)에 대해 double black을 처리해주고 나서 self._size를 1빼준다.
    target의 successor가 그 부모의 왼쪽인 경우에는 target의 successor에 왼쪽 자식이 더 이상 없다고 생각하면 되고 이 경우 역시 target의 successor의 오른쪽 자식이 있는지 없는지에 따라 경우를 나누고 앞서 진행한 방식(successor가 그 부모의 오른쪽인 경우)과 유사한 방식으로 delete 과정을 거쳐준다.
    target의 successor의 색상이 블랙이 아닌 경우에는 target의 successor가 블랙인 경우에서 double black 처리를 빼고 같은 방식을 거쳐 delete 과정을 진행해주면 된다.
    
    case3: target에 한쪽 자식만 있는 경우이며 target이 루트인 경우에는 target 자식의 부모를 None으로 target의 element를 None으로 설정해주고 root를 target의 자식으로 설정해주고 그 컬러를 black으로 한뒤 self._size를 1 빼준다. target이 루트가 아닌 경우에는 target의 색이 블랙인지에 따라 double black처리를 먼저 target 자리에서 해주고 (블랙이 아니라면 하지 않고) target의 자식의 parent를 target의 parent로 설정하고 target의 parent의 자식 자리를 (기존 target 자리를) target의 자식에게 지정한다. 그리고 self._size를 1빼준다.
    
    :param element: 지우고자 하는 target 노드의 element
    :return: 지운 target 노드의 element
    """
    def delete(self, element):        
        target = self._search_for_delete(element)
        A = target._element
        if target._right == None and target._left == None:
            if target == self._root:
                target._element = None
                self._root = None
                self._size -= 1
                
            elif target._color == self._Node.BLACK:
                self._process_double_black(target)
                if target._parent._right == target:
                    target._parent._right = None
                elif target._parent._left == target:
                    target._parent._left = None
                self._size -= 1
                
            else:
                if target._parent._left == target:
                    target._parent._left = None
                    self._size -= 1
                elif target._parent._right == target:
                    target._parent._right = None
                    self._size -= 1
                    
        elif target._right != None and target._left != None:

            if self._successor(target)._color == self._Node.BLACK:
                if self._successor(target) == self._successor(target)._parent._right:
                    if self._successor(target)._right == None:
                        target._element = self._successor(target)._element
                        target = self._successor(target)
                        self._process_double_black(target)
                        if target == target._parent._left:
                            target._parent._left = None
                        else:
                            target._parent._right = None
                        self._size -= 1 
                    elif self._successor(target)._right != None:
                        target._element = self._successor(target)._element
                        target = self._successor(target)
                        target._right._parent = target._parent
                        target._parent._right = target._right
                        self._process_double_black(target._parent._right)
                        self._size -= 1 
                        
                elif self._successor(target) == self._successor(target)._parent._left:
                    if self._successor(target)._right == None:
                        target._element = self._successor(target)._element
                        target = self._successor(target)
                        self._process_double_black(target)
                        if target == target._parent._left:
                            target._parent._left = None
                        else:
                            target._parent._right = None
                        self._size -= 1 
                    elif self._successor(target)._right != None:
                        target._element = self._successor(target)._element
                        target = self._successor(target)
                        target._right._parent = target._parent
                        target._parent._left = target._right
                        self._process_double_black(target._parent._left)
                        self._size -= 1 

            elif self._successor(target)._color == self._Node.RED:
                if self._successor(target) == self._successor(target)._parent._right:
                    if self._successor(target)._right == None:
                        target._element = self._successor(target)._element
                        target = self._successor(target)
                        target._parent._right = None
                        self._size -= 1 
                    elif self._successor(target)._right != None:
                        target._element = self._successor(target)._element
                        target = self._successor(target)
                        target._right._parent = target._parent
                        target._parent._right = target._right
                        self._size -= 1 
                elif self._successor(target) == self._successor(target)._parent._left:
                    if self._successor(target)._right == None:
                        target._element = self._successor(target)._element
                        target = self._successor(target)
                        target._parent._left = None
                        self._size -= 1 
                    elif self._successor(target)._right != None:
                        target._element = self._successor(target)._element
                        target = self._successor(target)
                        target._right._parent = target._parent
                        target._parent._left = target._right
                        self._size -= 1 
                        
        elif target._right != None and target._left == None:
            if target == self._root: 
                target._right._parent = None
                
                target._element = None 
                
                self._root = target._right
                self._root._color = self._Node.BLACK
                self._size -= 1
                
            elif target._color == self._Node.BLACK:
                self._process_double_black(target)
                target._right._parent = target._parent
                if target._parent._right == None: 
                    target._parent._left = target._right 
                    self._size -= 1
                elif target._parent._left == None: 
                    target._parent._right = target._right 
                    self._size -= 1
                elif target._parent._right == target:
                    target._parent._right = target._right
                    self._size -= 1
                else:
                    target._parent._left = target._right
                    self._size -= 1
            else:
                target._right._parent = target._parent
                if target._parent._right == None: 
                    target._parent._left = target._right 
                    self._size -= 1
                elif target._parent._left == None: 
                    target._parent._right = target._right 
                    self._size -= 1
                elif target._parent._right == target:
                    target._parent._right = target._right
                    self._size -= 1
                else:
                    target._parent._left = target._right
                    self._size -= 1
                
            
        elif target._right == None and target._left != None:
            if target == self._root: 
                target._left._parent = None
                
                target._element = None 
                
                self._root = target._left
                self._root._color = self._Node.BLACK
                self._size -= 1
                
            elif target._color == self._Node.BLACK:
                self._process_double_black(target)
                target._left._parent = target._parent
                if target._parent._right == None: 
                    target._parent._left = target._left 
                    self._size -= 1
                elif target._parent._left == None: 
                    target._parent._right = target._left 
                    self._size -= 1
                elif target._parent._right == target:
                    target._parent._right = target._left
                    self._size -= 1
                else:
                    target._parent._left = target._left
                    self._size -= 1
            else:
                target._left._parent = target._parent
                if target._parent._right == None: 
                    target._parent._left = target._left 
                    self._size -= 1
                elif target._parent._left == None: 
                    target._parent._right = target._left 
                    self._size -= 1
                elif target._parent._right == target:
                    target._parent._right = target._left
                    self._size -= 1
                else:
                    target._parent._left = target._left
                    self._size -= 1
        
        return A
    
    """
    _search_for_delete(self,element)는 기존 search(self,element)와 유사한 구조를 가지고 있지만 element가 아닌 노드를 return하기 위한 목적으로 구현된 self._sub_search_for_delete과 연결되어 있다는 점에서 다르다. 결론적으로 이 함수 역시 루트가 None, 즉 트리가 비어있다면 None을 return하고 그렇지 않은 경우에 self._sub_search_for_delete을 호출한다.
    
    :param element: 지우기 이전에 찾는 단계에서 찾고자 하는 노드의 element를 의미한다.
    :return: 노드를 찾지 못한다면 None을 return, self._sub_search_for_delete에 의해서 노드를 찾는다면 해당 노드를 return 한다.
    """
    def _search_for_delete(self, element):
        if self._root == None:
            return None
        else:
            return self._sub_search_for_delete(self._root, element)
    
    """
    _sub_search_for_delete(self,node,element)는 _search_sub과 그 과정이 거의 동일하나 찾은 노드의 element가 아닌 노드를 return 한다는 점에서 차이가 있다. (따라서 과정에 대한 설명은 _search_sub을 참고하면 이해할 수 있다.)
    
    :param node: search 시점의 노드
    :param element: 찾고자 하는 노드의 element
    :return: 노드를 찾는다면 노드를 return, 찾지 못한다면 None을 return
    """
    def _sub_search_for_delete(self, node, element):
        if node._element == element:
            return node
        elif node._element < element:
            if node._right == None:
                return None
            else:
                return self._sub_search_for_delete(node._right, element)
        elif node._element > element:
            if node._left == None:
                return None
            else:
                return self._sub_search_for_delete(node._left, element)
    """
    _process_double_black(self, node)는 node 자리에서 발생한 double black을 처리하기 위한 함수이다. 우선 이 노드에서 처음 조건문으로 self._sibiling이 None인지를 확인하는데 만약 None인 경우에는 node를 포함한 subtree의 반대편 subtree에 노드가 없음을 의미하므로 double black 처리가 필요해지지 않는 상황이 되어서 pass 처리를 해준다.
    노드의 형제노드가 None이 아니라면 그 형제노드의 색상이 블랙인지 레드인지에 따라 나누고 블랙인 경우에는 그 형제노드의 자식이 모두 블랙인지(여기선, 블랙인 경우에는 None인 경우를 포함) 아니면 그 자식들 중 레드가 있는지에 따라서 경우를 다시 나누어 처리를 하게 된다. 여기서 이 경우의 수에 따른 처리에 따라 형제노드의 색상이 블랙이며 형제 노드가 red 자식을 가지는 경우를 _process_double_black_01로 처리하였으며 형제노드의 색상이 블랙이며 형제 노드의 자식이 모두 black인 경우에 대해서 _process_double_black_02로 처리하였다. 그리고 형제노드의 색상이 red인 경우에는 _process_double_black 내부에서 처리하였다.
    
    case1: 형제 노드의 색상이 블랙인 경우
    형제 노드의 자식이 모두 None인 경우에는 self._process double_black_02를 호출한다.
    형제 노드가 한쪽 자식만 있는 경우에는 그 자식의 색상이 red이면 self._process_double_black_01을 호출하고 black이면 self._process_double_black_02를 호출한다.
    형제노드의 자식이 두명 모두 있는 경우에는 그 자식 두명의 색상이 모두 블랙인 경우일때 self._process_double_black_02를 호출하고 두 자식 중 한명이라도 red인 경우일때 self._process_double_black_01을 호출한다.
    
    case2: 형제 노드의 색상이 레드인 경우
    형제 노드의 색상을 black으로 바꾸고 형제 노드의 부모의 색상을 red로 바꾸고 형제 노드 위치에서 rotate를 진행한다. (형제 노드와 형제 노드의 부모 사이의 관계가 바뀜) 그 뒤에 노드 자리에서 다시 self._process_double_black을 호출하여 double black 상황에 대해 처리한다. (rotate를 한다고 해도 node 자리에서는 double black 상황이 유지되기 때문)
    
    :param node: double black 상황에 처해서 이를 처리해줘야 하는 위치의 노드를 의미한다.
    """
    def _process_double_black(self, node):
        if self._sibiling(node) == None:
            pass
        elif self._sibiling(node)._color == self._Node.BLACK:
            if self._sibiling(node)._right == None and self._sibiling(node)._left == None:
                self._process_double_black_02(node)
            elif self._sibiling(node)._left != None and self._sibiling(node)._right == None:
                if self._sibiling(node)._left._color == self._Node.BLACK:
                    self._process_double_black_02(node)
                elif self._sibiling(node)._left._color == self._Node.RED:
                    self._process_double_black_01(node)
            elif self._sibiling(node)._left == None and self._sibiling(node)._right != None:
                if self._sibiling(node)._right._color == self._Node.BLACK:
                    self._process_double_black_02(node)
                elif self._sibiling(node)._right._color == self._Node.RED:
                    self._process_double_black_01(node)
            elif self._sibiling(node)._left != None and self._sibiling(node)._right != None:
                if self._sibiling(node)._left._color == self._Node.BLACK and self._sibiling(node)._right._color == self._Node.BLACK:
                    self._process_double_black_02(node)
                if self._sibiling(node)._left._color == self._Node.RED or self._sibiling(node)._right._color == self._Node.RED:
                    self._process_double_black_01(node)
                
        elif self._sibiling(node)._color == self._Node.RED:
            self._sibiling(node)._color = self._Node.BLACK
            self._sibiling(node)._parent._color = self._Node.RED
            self._rotate(self._sibiling(node))
            self._process_double_black(node)
            
    
    """
    _process_double_black_01(self,node)는 형제 노드가 블랙이며 그 자식 중에 red가 있을때에 대한 처리를 수행하는 함수이다. 이 함수의 기능을 수행하기 위해서 우선 형제노드의 자식 중 한쪽이 None인 경우(case1)와 두 자식 모두 None이 아닌 경우(case2)로 나누었다.
    
    case1: 형제노드의 자식 중 한쪽이 None인 경우에서는 형제노드의 다른쪽 자식이 red인 경우의 수 밖에 없고 이에 따라 형제노드의 색상이 red인 자식의 위치에서 reconstruct를 수행하면 된다. reconstruct를 수행하기 전에 reconstruct 이후의 결과에서 기존 형제 노드 위치의 부모가 되는 노드는 기존 형제 노드 위치의 부모의 색상을 그대로 가져오고 나머지 노드들은 black의 색상이어야 한다.
    case2: 이 경우에는 형제노드의 자식 중 어떤 쪽이 red인지에 따라 조건문을 이용해 경우의 수를 나누어주어서 조건문에서 그 색상이 red로 확인된 자식의 위치에서 reconstruct를 하게 되는 것이고 색상을 재배치하는 것은 case1에서와 같은 방식으로 진행하면 된다.
    
    :param node: 더블 블랙 상황에 처해있으며 형제 노드가 블랙이고 그 자식 중 red 색상이 있는 경우의 노드를 의미한다.
    """
    def _process_double_black_01(self, node):
        if self._sibiling(node)._left == None:
            if self._sibiling(node) == self._sibiling(node)._parent._left:
                self._sibiling(node)._right._color = self._sibiling(node)._parent._color
                self._sibiling(node)._parent._color = self._Node.BLACK
                self._reconstruct(self._sibiling(node)._right)

            elif self._sibiling(node) == self._sibiling(node)._parent._right:
                self._sibiling(node)._right._color = self._Node.BLACK
                self._sibiling(node)._color = self._sibiling(node)._parent._color
                self._sibiling(node)._parent._color = self._Node.BLACK
                self._reconstruct(self._sibiling(node)._right)

        elif self._sibiling(node)._right == None:
            if self._sibiling(node) == self._sibiling(node)._parent._left:
                self._sibiling(node)._left._color = self._Node.BLACK
                self._sibiling(node)._color = self._sibiling(node)._parent._color
                self._sibiling(node)._parent._color = self._Node.BLACK
                self._reconstruct(self._sibiling(node)._left)

            elif self._sibiling(node) == self._sibiling(node)._parent._right:
                self._sibiling(node)._left._color = self._sibiling(node)._parent._color
                self._sibiling(node)._parent._color = self._Node.BLACK
                self._reconstruct(self._sibiling(node)._left)
        elif self._sibiling(node)._right != None and self._sibiling(node)._left != None:
            if self._sibiling(node)._parent._left == self._sibiling(node):
                
                if self._sibiling(node)._right._color == self._Node.RED:
                    self._sibiling(node)._right._color = self._sibiling(node)._parent._color 
                    self._sibiling(node)._color = self._Node.BLACK # 수정됨
                    self._sibiling(node)._parent._color = self._Node.BLACK
                    self._reconstruct(self._sibiling(node)._right)
                elif self._sibiling(node)._left._color == self._Node.RED:
                    self._sibiling(node)._left._color = self._Node.BLACK # 수정됨
                    self._sibiling(node)._color = self._sibiling(node)._parent._color 
                    self._sibiling(node)._parent._color = self._Node.BLACK
                    self._reconstruct(self._sibiling(node)._left)
            else:
                if self._sibiling(node)._right._color == self._Node.RED:
                    self._sibiling(node)._right._color = self._Node.BLACK # 수정됨
                    self._sibiling(node)._color = self._sibiling(node)._parent._color 
                    self._sibiling(node)._parent._color = self._Node.BLACK
                    self._reconstruct(self._sibiling(node)._right)
                elif self._sibiling(node)._left._color == self._Node.RED:
                    self._sibiling(node)._left._color = self._sibiling(node)._parent._color 
                    self._sibiling(node)._color = self._Node.BLACK # 수정됨
                    self._sibiling(node)._parent._color = self._Node.BLACK
                    self._reconstruct(self._sibiling(node)._left)
    """
    _process_double_black_02(self,node)는 형제 노드의 색상이 블랙이고 그 자식도 모두 블랙의 색상을 가지는 경우에 double black을 처리하는 기능을 가진 함수이다. 이 경우에서는 double black 상황에 처한 노드의 부모의 색상을 black으로, 형제 노드의 색상은 red로 바꾸어 주어야 하는데 만약 노드의 부모가 처음부터 블랙인 상황이었다면 부모 노드의 자리에서 아직도 double black에 놓인 상황이므로 여기서 끝나지 않고 부모 노드의 자리에서 다시 double black을 처리해줘야 한다. 하지만, 이중에서도 만약 부모 노드가 트리의 root 자리여서 블랙인 경우에는 전체 트리의 height이 1 감소하면 되는 것이므로 double black을 위반하지 않는 상황이 되어서 형제 노드의 색상을 red로 처리하는 것으로 double black 처리를 마무리 지을 수 있고 이는 이 함수의 첫 조건문에서 구현되어 있다. 그 뒤 조건문에서의 처리도 살펴보자면, 부모 노드의 색상이 블랙인 경우 앞서 설명한 것처럼 형제 노드의 색상만 레드로 바꾸어주고 부모 노드의 자리에서 self,_process_double_black을 호출한다. 부모 노드의 색상이 레드인 경우에는 형제 노드의 색상을 레드로, 부모 노드의 색상을 블랙으로 해줘서 double black 상황에 대한 처리를 완료한다.
    :param node: double black 상황에 놓인 노드로, 그 형제 노드의 색상이 black이고 그 자식 노드의 색상도 모두 black인 노드를 의미한다.
    """
    def _process_double_black_02(self, node):
        if node._parent == self._root:
            self._sibiling(node)._color = self._Node.RED
        else:
            if node._parent._color == self._Node.BLACK:
                self._sibiling(node)._color = self._Node.RED
                self._process_double_black(node._parent)
            elif node._parent._color == self._Node.RED:
                self._sibiling(node)._color = self._Node.RED
                node._parent._color = self._Node.BLACK
        
    """
    _reconstruct(self, node)는 node와 node의 부모, node의 부모의 부모 사이의 연결 관계를 재정립하는 기능을 수행하는 함수로 만약 node와 node의 부모사이의 관계(왼쪽 child인지, 오른쪽 child인지)가 node의 부모와 node의 부모의 부모사이의 관계(왼쪽 child인지, 오른쪽 child인지)에서 유지되지 않으면 node자리에서 rotate를 두번 수행하게 되고 그 두 관계가 유지되면 node._parent 자리에서 rotate를 한번 수행하면 된다.
    
    :param node: reconstruct를 하고자하는 위치의 node를 의미한다.
    """
    def _reconstruct(self, node):
        if node._parent._right == node and node._parent._parent._right == node._parent:
            self._rotate(node._parent)
        
        elif node._parent._right == node and node._parent._parent._left == node._parent:
            self._rotate(node)
            self._rotate(node)
            
        elif node._parent._left == node and node._parent._parent._left == node._parent:
            self._rotate(node._parent)
        
        elif node._parent._left == node and node._parent._parent._right == node._parent:
            self._rotate(node)
            self._rotate(node)
        
    """
    _rotate(self, node)는 node와 node 부모 사이의 관계를 재정립하는 함수를 의미한다. 즉 노드의 부모가 노드의 자식이 되고 노드가 기존 노드의 부모의 부모가 된다. 이를 코드로 구현하면 다음과 같다.
    우선, 노드가 그 노드 부모의 왼쪽 자식인지 오른쪽 자식인지 부터 노드와 노드 부모의 오른쪽 자식 간에 비교를 통해 나눈다. 해당 함수에서는 이 비교가 많이 이루어질 것이라고 생각하여서 self._node_is_right를 따로 구현하고 호출하여 좀 더 가시적으로 확인하고 이해를 쉽게 할 수 있게 하였다. 
    이 코드의 경우에는 node가 node 부모의 왼쪽 자식인 경우(case1)부터 살펴보고 그 뒤에 오른쪽 자식인 경우(case2)를 살펴본다.
    
    case1: 노드가 부모 노드의 왼쪽 자식이었을 경우인 이 경우에서는 우선 child 변수와 parent 변수를 설정한다. 그리고 이 parent가 self._root에 해당하는지, 그렇지 않은지에 따라서 나눈다. 이렇게 나누어주는 이유는 parent가 self._root일 경우 self._root이 아닐 경우에 parent._parent의 자식으로 이어주는 코드를 또 작성해야 되는데 self._root인 경우에는 그렇게 하지 않고 그저 self._root으로 child를 설정해주면 되기 때문이다. parent가 self._root인 경우의 코드에 대해 다시 보면, child의 right이 있는 경우(right만 보는 이유는 노드가 부모 노드의 왼쪽 노드였기 때문) child의 right의 부모를 parent로 연결해주고 parent의 왼쪽 자식 역시 child의 right으로 업데이트 해준다. 그리고 child의 parent는 기존 parent의 parent로 업데이트를 해주고 앞선 설명에서 설명하였던 것 처럼 self._root을 child로 바꾼다.
    parent가 self._root가 아닌 경우에서도 앞선 경우에서처럼 child의 right의 parent를 업데이트하는 것, parent의 left를 child의 right으로 업데이트하는 것, child의 parent의 기존 parent의 parent로 업데이트하는 것은 동일하다. 그러나 이 경우에는 parent의 parent의 자식도 다시 업데이트를 해주어야 하므로 오른쪽 자식인지 왼쪽 자식인지에 따라 child로 업데이트를 해준다. 이후에는 child의 right을 parent로 업데이트, parent의 parent를 child로 업데이트 해준다.
    
    case2: 이 경우는 노드가 부모 노드의 오른쪽 자식이었을 경우로, 어떤 노드의 자식을 업데이트 해줄때 오른쪽 왼쪽 자식의 관계만 case1에서와 반대로 해주면 rotate 기능을 수행하는 코드를 정상적으로 실행시킬 수 있다.
    
    :param node: 이 노드와 부모 노드의 관계를 재정립하는 rotate 기능을 수행시키고자 하는 그 노드를 의미한다.
    
    """
    def _rotate(self,node):
        
        if not self._node_is_right(node):
            child = node
            parent = child._parent
            if parent == self._root:
                if child._right:
                    child._right._parent = parent
                parent._left = child._right
                child._parent = parent._parent

                self._root = child

                
            else:
                if child._right:
                    child._right._parent = parent
                parent._left = child._right
                child._parent = parent._parent
                
                if self._node_is_right(parent):
                    parent._parent._right = child
                elif not self._node_is_right(parent) :
                    parent._parent._left = child
            
            child._right = parent
            parent._parent = child
            
        elif self._node_is_right(node):
            child = node
            parent = child._parent
            
            if parent == self._root:
                if child._left:
                    child._left._parent = parent
                parent._right = child._left
                child._parent = parent._parent

                self._root = child
            else:
                if child._left:
                    child._left._parent = parent
                parent._right = child._left
                child._parent = parent._parent
                if self._node_is_right(parent):
                    parent._parent._right = child
                elif not self._node_is_right(parent):
                    parent._parent._left = child
                
            child._left = parent
            parent._parent = child
            
    """
    _node_is_right(self, node)의 경우 rotate에서 node가 node의 parent의 왼쪽 자식인지 오른쪽 자식인지 쉽게 구분하는데 사용하기 위해 만든 함수로, node가 node의 parent의 오른쪽 자식이면 True, 그렇지 않으면 False를 return 한다.
    :param node: parent의 오른쪽 child인지 왼쪽 child인지 확인하고 싶은 노드를 의미한다.
    :return: parent의 오른쪽 child이면 True return, 왼쪽 child이면 False를 return한다.
    """
    def _node_is_right(self, node):
        if node == node._parent._right:
            return True
        elif node == node._parent._left:
            return False
            
    """
    _recoloring_for_insert(self, node)는 부모의 형제 노드의 색상이 red인 경우에 split에 해당하는 recoloring 작업을 수행해주는 함수이다. 먼저 node._parent._parent가 self._root인 경우에는 root 자리는 black 색상이 들어가야 하기 때문에 node._parent._parent 자리에 대한 recoloring은 하지 않고 node._parent._color를 black으로, 부모의 형제노드의 색상을 black으로 지정한다. node._parent._parent가 self._root가 아닌 경우에는 node._parent._parent의 color를 red로 지정, 나머지 컬러는 앞선 경우와 동일하게 지정한다.
    
    :param node: 리컬러링이 요구되는 조건에 부합하는 환경에 insert된 노드
    """
    def _recoloring_for_insert(self, node):
        if node._parent._parent == self._root:
            node._parent._color = self._Node.BLACK
            self._sibiling(node._parent)._color = self._Node.BLACK
        else:
            node._parent._color = self._Node.BLACK
            self._sibiling(node._parent)._color = self._Node.BLACK
            node._parent._parent._color = self._Node.RED
        
        
         
        
    # BONUS FUNCTIONS -- use them freely if you want
    def _is_black(self, node):
        return node == None or node._color == self._Node.BLACK

    def _successor(self, node):
        successor = node._right
        while successor._left != None:
            successor = successor._left
        return successor

    def _sibiling(self, node):
        parent = node._parent

        if parent._left == node:
            return parent._right
        else:
            return parent._left

    # Supporting functions -- DO NOT MODIFY BELOW
    def display(self):
        print('--------------')
        self._display(self._root, 0)
        print('--------------')

    def _display(self, node, depth):
        if node == None:
            return

        if node._right != None:
            if node._right._parent != node:
                print("parent-child error - ", node._element, node._right._element)
            self._display(node._right, depth+1)

        if node == self._root:
            symbol = '>'
        else:
            symbol = '*'

        if node._color == self._Node.RED:
            colorstr = 'R'
        else:
            colorstr = 'B'
        print(f'{"    "*depth}{symbol} {node._element}({colorstr})')
        if node._left != None:
            if node._left._parent != node:
                print("parent error - ", node._element, node._left._element)
            self._display(node._left, depth+1)

    def inorder_traverse(self):
        return self._inorder_traverse(self._root)

    def _inorder_traverse(self, node):
        if node == None:
            return []
        else:
            return self._inorder_traverse(node._left) + [node._element] + self._inorder_traverse(node._right)

    def check_tree_property_silent(self):
        if self._root == None:
            return True

        if not self._check_parent_child_link(self._root):
            print('Parent-child link is violated')
            return False
        if not self._check_binary_search_tree_property(self._root):
            print('Binary search tree property is violated')
            return False
        if not self._root._color == self._Node.BLACK:
            print('Root black property is violated')
            return False
        if not self._check_double_red_property(self._root):
            print('Internal property is violated')
            return False
        if self._check_black_height_property(self._root) == 0:
            print('Black height property is violated')
            return False
        return True

    def check_tree_property(self):
        if self._root == None:
            print('Empty tree')
            return

        print('Checking binary search tree property...')
        self._check_parent_child_link(self._root)
        self._check_binary_search_tree_property(self._root)
        print('Done')

        print('Checking root black property...')
        print(self._root._color == self._Node.BLACK)
        print('Done')

        print('Checking internal property (=no double red)...')
        self._check_double_red_property(self._root)
        print('Done')

        print('Checking black height property...')
        self._check_black_height_property(self._root)
        print('Done')

    def _check_parent_child_link(self, node):
        if node == None:
            return True

        test_pass = True

        if node._right != None:
            if node._right._parent != node:
                print("parent-child error - ", node._element, node._right._element)
            test_pass = test_pass and self._check_parent_child_link(node._right)
        if node._left != None:
            if node._left._parent != node:
                print("parent error - ", node._element, node._left._element)
            test_pass = test_pass and self._check_parent_child_link(node._left)

        return test_pass

    def _check_binary_search_tree_property(self, node):
        if node == None:
            return True

        test_pass = True

        if node._left != None:
            if node._left._element > node._element:
                print("Binary search tree property error - ", node._element, node._left._element)
                return False
            test_pass = test_pass and self._check_binary_search_tree_property(node._left)

        if node._right != None:
            if node._right._element < node._element:
                print("Binary search tree property error - ", node._element, node._right._element)
                return False
            test_pass = test_pass and self._check_binary_search_tree_property(node._right)

        return test_pass

    def _check_double_red_property(self, node):
        if node == None:
            return True

        test_pass = True

        if node._color == self._Node.RED:
            if node._left != None:
                if node._left._color == self._Node.RED:
                    print("Double red property error - ", node._element, node._left._element)
                    return False
            if node._right != None:
                if node._right._color == self._Node.RED:
                    print("Double red property error - ", node._element, node._right._element)
                    return False

        if node._left != None:
            test_pass = test_pass and self._check_double_red_property(node._left)
        if node._right != None:
            test_pass = test_pass and self._check_double_red_property(node._right)

        return test_pass


    def _check_black_height_property(self, node):
        if node == None:
            return 1

        left_height = self._check_black_height_property(node._left)
        right_height = self._check_black_height_property(node._right)

        if left_height != right_height:
            print("Black height property error - ", node._element, left_height, right_height)
            return 0

        if node._color == self._Node.BLACK:
            return left_height + 1
        else:
            return left_height