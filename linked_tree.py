from tree import Tree

"""
Class LinkedTree(Tree)의 경우, 상위 클래스인 Tree로 부터 상속된 하위 클래스 LinkedTree임을 의미하며 이에 따라 상위 클래스인 Tree의 method들과 attributes들을 상속받아 사용이 가능하다.

:param Tree: 상위 클래스인 Tree를 가리킨다.
"""
class LinkedTree(Tree):
    """Linked representation of a general tree structure."""

    #-------------------------- nested _Node class --------------------------
    class _Node:
        """Lightweight, nonpublic class for storing a node."""
        
        """
        __slots__의 경우에는 member variable인 '_element', '_parent', '_children'을 위해서 memory space를 assign한다. 이 경우, 메모리 공간과 퍼포먼스 측면에서 이득을 얻을 수 있으며 부수적 효과로 변수명에서의 오류를 막을 수 있다.
        """
        __slots__ = '_element', '_parent', '_children' # streamline memory usage

        """
        __init__의 경우에는 object를 만들때 사용되는 컨스트럭터이며 객체의 초기값인 element, parent, children을 이 컨스트럭터를 통해 설정할 수 있다. 또한 element, parent, children 앞에 underscore character가 있는 것을 확인할 수 있어 encapsulation 개념이 적용되어 있는 것을 볼 수 있다.
        
        :param element: node에 저장할 element를 의미한다.
        :param parent: node의 parent에 해당하는 node를 가리키는 reference다. default값은 None이다.
        :param children: node의 children에 대한 reference들로 이루어진 리스트이다. default값은 None이다.
        """
        def __init__(self, element, parent=None, children=None):
            self._element = element # the element of this node
            self._parent = parent # a link towards the parent
            if children == None:
                self._children = []
            else:
                self._children = children # list of links towards children nodes

    #-------------------------- nested Position class --------------------------
    """
    Class Position의 경우에는 Tree 클래스 내에서 정의된 Position 클래스를 상위 클래스로 하는 클래스이다. 해당 상위 클래스로부터 method와 attributes를 상속받을 수 있다. 또한 Position 클래스는 노드의 위치를 나타내는 추상화된 클래스이다.
    
    :param Tree.Position: Position 클래스의 상위 클래스이다.
    """
    class Position(Tree.Position):
        """An abstraction representing the location of a single element."""
        
        """
        이 클래스의 __init__도 컨스트럭터의 역할이며 초기값인 container와 node를 이를 통해 설정 가능하다. 또한, container와 node 앞에 underscore character가 있는 것을 통해 encapsulation 개념이 적용되어있음을 확인할 수 있다.
        
        :param container: 그 position의 node를 담고 있는 Tree를 의미한다.
        :param node: 해당 position의 위치를 가리키는 node object를 가리킨다.
        """
        def __init__(self, container, node):
            """Constructor should not be invoked by user."""
            self._container = container
            self._node = node
        
        """
        element(self)는 position에 저장된 노드의 element를 반환하는 역할을 한다. 이를 통해, node의 position을 알면 node의 element를 가져오는 것도 가능해진다.
        
        :return: position에 저장된 노드의 element를 반환
        """
        def element(self):
            """Return the element stored at this Position."""
            return self._node._element

        """
        __eq__(self, other)의 경우, 다른 position과의 비교를 통해 만약 두 position이 같은 객체를 가리키는 것이 확인되고 type이 같은지가 확인되면 True를 반환한다. 즉, 두 position 객체가 같은 객체인지 확인하는 역할을 수행하며 이러한 역할이 필요로 되는 경우에 사용되는 목적성을 가지고 있다.
        
        :param other: 비교하고자 하는 객체를 가리킨다.
        :return: equal 여부에 대한 boolean value
        """
        def __eq__(self, other):
            """Return True if other is a Position representing the same location."""
            return type(other) is type(self) and other._node is self._node

    #------------------------------- utility methods -------------------------------
    """
    _validate(self, p)는 p position을 받고 그 position에서의 노드를 return하는 기능을 가지고 있다. 좀 더 자세히 말하자면, isinstance를 통해 p가 self.Position의 객체인지 확인하는 단계(그렇지 않을시 TypeError를 raise하며 'p must be proper Position type'라는 문자열을 뱉음)와 p position의 container가 tree 객체인 self와 일치하는지 확인하는 단계(그렇지 않을시 ValueError를 raise하며 'p does not belong to this container'라는 문자열을 뱉음)와 p position 노드의 parent와 p position 노드가 같은지 확인하는 단계, 즉 p가 더 이상 사용되지 않는, deprecated한 노드인지를 확인하는 단계(그렇지 않을시 ValueError를 raise하며 'p is no longer valid'라는 문자열을 뱉음)를 거치고 이 모든 단계를 통해 유효성이 확인된 경우 p position에 해당하는 node를 반환하게 된다.
    
    :param p: position p 객체를 가리킨다.
    :return: position p에 해당하는 노드를 반환
    :raises TypeError: p가 self.Position의 객체가 아닌 경우
    :raises ValueError: p의 container가 tree 객체인 self와 일치하지 않는 경우, p가 deprecated한 노드인 경우
    
    """
    def _validate(self, p):
        """Return associated node, if position is valid."""
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._node._parent is p._node:            # convention for deprecated nodes
            raise ValueError('p is no longer valid')
        return p._node

    """
    _make_position(self,node)는 입력받은 node가 None이 아닐 경우, 해당 node의 position 객체를 반환해주는 역할을 한다. 그렇지 않을 경우, None을 반환하게 된다.
    
    :param node: position을 알고 싶은 node 객체를 가리킨다.
    :return: 받은 node의 position 객체를 반환(node가 None이 아닐 경우), 그렇지 않다면 None을 반환
    """
    def _make_position(self, node):
        """Return Position instance for given node (or None if no node)."""
        return self.Position(self, node) if node is not None else None

    #-------------------------- Tree constructor --------------------------
    """
    아래 __init__(self)는 LinkedBinaryTree의 컨스트럭터이며, 초기값으로써 empty binary tree를 생성한다. 다시 말해서, self._root에 None을 assign하고 self._size에 0을 assign하여 root node와 size에 대해 초기화한다.
    """
    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = None
        self._size = 0

    #-------------------------- public accessors --------------------------    
    """
    root(self)는 tree 객체의 root position을 반환하는 역할(self._make_position을 이용)을 하며 tree가 empty하다면 None을 반환한다.
    
    :return: tree 객체의 root position을 반환, 만약 tree가 empty라면 None을 반환
    """
    def root(self):
        """Return the root Position of the tree (or None if tree is empty)."""
        return self._make_position(self._root)
    
    """
    parent(self,p)는 p가 root position이 아닐 경우, position p에 대한 부모 노드의 position을 반환한다. (p가 root position인 경우, None을 반환한다.) position p의 부모 노드를 알아내기 위해서 우선 self._validate(p)를 통해 position p에 해당하는 노드를 알아내고 나서 node._parent로 parent 노드를 찾고 self._make_position을 이용해 parent node에 해당하는 position을 알아낸다. self._validate를 이용하므로 self._validate에서 raise되는 error가 self._validate와 동일한 특정 조건 아래에서 raise 될 수 있다.
    
    :param p: position p 객체를 가리킨다.
    :return: p가 root position이 아닐 경우에 position p에 대한 부모 노드의 position을 return, p가 root postion인 경우에는 None을 반환
    :raises TypeError: p가 self.Position의 객체가 아닌 경우
    :raises ValueError: p의 container가 tree 객체인 self와 일치하지 않는 경우, p가 deprecated한 노드인 경우
    """
    def parent(self, p):
        """Return the Position of p's parent (or None if p is root)."""
        node = self._validate(p)
        return self._make_position(node._parent)

    """
    num_children(self,p)는 p position에 해당하는 node의 children node에 해당하는 node들의 수를 반환한다. 이를 위해서, self._validate을 이용하여 p position에 해당하는 node 객체를 알아내고 node._children을 통해 알아낸 children 노드의 수를 len을 이용하여 return한다. self._validate를 이용하므로 self._validate에서 raise되는 error가 self._validate와 동일한 특정 조건 하에 raise 가능하다.
    
    :param p: children 노드의 수를 알아내고 싶은 position p를 가리킨다.
    :return: position p에 해당하는 노드의 children 노드의 수를 반환한다.
    :raises TypeError: p가 self.Position의 객체가 아닌 경우
    :raises ValueError: p의 container가 tree 객체인 self와 일치하지 않는 경우, p가 deprecated한 노드인 경우
    """
    def num_children(self, p):
        """Return the number of children of Position p."""
        node = self._validate(p)
        return len(node._children)
    
    """
    children(self, p)는 p position에 해당하는 node의 child node의 position을 yield한다. 이를 위해서, self._validate를 통해 알아낸 p position의 노드 객체를 node라고 하고 node._children에 대해 반복문을 걸어서 나오는 child에 self._make_position을 하여 나온 position을 yield한다. self._validate를 이용하므로 self._validate에서 raise되는 error가 self._validate와 동일한 특정 조건 하에 raise 가능하다.
    
    :param p: children의 position들을 알아내고 싶은 노드의 position p를 가리킨다.
    :yield: p의 children에 대해 child의 position을 yield한다.
    :raises TypeError: p가 self.Position의 객체가 아닌 경우
    :raises ValueError: p의 container가 tree 객체인 self와 일치하지 않는 경우, p가 deprecated한 노드인 경우
    """
    def children(self, p):
        node = self._validate(p)
        for child in node._children:
            yield self._make_position(child)

    """
    __len__(self)는 tree 객체에 저장된 요소의 총 개수를 self._size를 이용해 반환한다.
    
    :return: tree 객체에 저장된 요소들의 총 개수를 반환한다.
    """
    def __len__(self):
        """Return the total number of elements in the tree."""
        return self._size    
    
    #-------------------------- nonpublic mutators --------------------------
    """
    _add_root(self,e) 메소드는 empty tree의 루트 자리에 element e를 가진 노드를 넣고 그 position을 반환한다. 이때, self._make_position(node)를 사용하여 node의 position을 알아내는 방안을 사용한다. tree가 empty하지 않다면, 즉 그 tree의 size가 0이 아니라면 'Root exists'라는 message와 함께 ValueError를 raise한다.
    
    :param e: tree의 root자리에 넣을 노드의 element
    :return: 새롭게 add된 root의 position 객체를 반환한다.
    :raises ValueError: tree가 empth하지 않은 경우, 'Root exises'라는 메세지와 함께
    """
    def _add_root(self, e):
        if self._size != 0:
            raise ValueError("Root exists")
        root = self._make_position(self._Node(e))
        self._root = root
        self._size = 1
        go = self.root()
        return go

    """
    _add_child(self, p, e)는 position p에 위치한 노드를 self._validate(p)를 통해 얻고 이를 pr, 즉 부모로 지정한 다음 child로 add하고 싶은 노드를 self._Node(e)로 만들고 ch._parent = pr을 통해 이 노드의 부모를 pr로 설정해준다. 그리고 나서 pr의 children list에 ch를 append 해주고 이에 따라 tree의 size가 늘어나는 것을 반영해주면 p position 노드에 element e를 갖는 child를 add하는 역할을 수행할 수 있다. 마지막에는 추가한 child의 position을 self._make_position으로 반환해준다.
    
    :param p: child를 add해줄 parent 노드의 position p 객체를 가리킨다.
    :param e: add되는 child node에 저장될 element e를 가리킨다.
    :return: 새롭게 추가된 child node의 position p 객체를 가리킨다.
    """
    def _add_child(self, p, e):
        pr = self._validate(p)
        ch = self._Node(e)
        ch._parent = pr
        pr._children.append(ch)
        self._size += 1
        return self._make_position(ch)

    """
    _replace(self,p,e) 메소드는 p position 객체의 노드를 self._validate(p)를 통해 얻고 이 노드의 element를 새로운 element인 e로 바꾸어주고 바꾸어주기 이전의 element는 return한다. 즉, 간단히 말해 이 메소드의 역할을 특정 포지션 노드의 element를 바꾸어주고 이전 element는 반환해주는 것이다.
    
    :param p: element를 바꾸어주고자 하는 노드의 position p 객체이다.
    :param e: position p에 위치한 노드에 대해서 해당 e element로 element를 바꾸어준다.
    :return: 바꾸어주기 이전의 old element를 return한다.
    """
    def _replace(self, p, e):
        aim = self._validate(p)
        result = aim._element
        aim._element = e
        return result

    """
    _delete(self,p)는 tree의 position p에 해당하는 노드를 지우고 지워진 노드의 element를 반환하는 역할을 수행한다. 우선, 해당 메소드는 children이 없는 leaf 노드만을 delete하므로 children의 수가 1 이상이면 ValueError를 raise하는 조건문을 거치게 된다. 해당 조건문 뒤로는 p position의 노드를 알기 위해서 self._validate(p)를 수행하고 그 노드의 parent를 찾은 뒤 그 parent의 children list에서 이전에 찾은 p position의 노드를 list의 remove로 제거한다. 마지막으로, tree의 size를 재조정해주고(delete했으니 1을 빼준다.) delete한 노드의 element를 반환한다.
    
    :param p: 지우고자 하는 노드의 position 객체
    :return: delete한 노드의 element
    :raises ValueError: p position node가 자식이 있는 경우
    """
    def _delete(self, p):
        if self.num_children(p) >= 1:
            raise ValueError
        aim = self._validate(p)
        pr = aim._parent
        pr._children.remove(aim)
        self._size -= 1
        return aim._element