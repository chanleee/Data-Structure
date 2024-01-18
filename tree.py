# Copyright 2013, Michael H. Goldwasser
#
# Developed for use with the book:
#
#        Data Structures and Algorithms in Python
#        Michael T. Goodrich, Roberto Tamassia, and Michael H. Goldwasser
#        John Wiley & Sons, 2013
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.    If not, see <http://www.gnu.org/licenses/>.

import collections
class Tree:
    """Abstract base class representing a tree structure."""

    #------------------------------- nested Position class -------------------------------
    class Position:
        """An abstraction representing the location of a single element within a tree.

        Note that two position instaces may represent the same inherent location in a tree.
        Therefore, users should always rely on syntax 'p == q' rather than 'p is q' when testing
        equivalence of positions.
        """

        def element(self):
            """Return the element stored at this Position."""
            raise NotImplementedError('must be implemented by subclass')

        def __eq__(self, other):
            """Return True if other Position represents the same location."""
            raise NotImplementedError('must be implemented by subclass')

        def __ne__(self, other):
            """Return True if other does not represent the same location."""
            return not (self == other)                        # opposite of __eq__

    # ---------- abstract methods that concrete subclass must support ----------
    def root(self):
        """Return Position representing the tree's root (or None if empty)."""
        raise NotImplementedError('must be implemented by subclass')

    def parent(self, p):
        """Return Position representing p's parent (or None if p is root)."""
        raise NotImplementedError('must be implemented by subclass')

    def num_children(self, p):
        """Return the number of children that Position p has."""
        raise NotImplementedError('must be implemented by subclass')

    def children(self, p):
        """Generate an iteration of Positions representing p's children."""
        raise NotImplementedError('must be implemented by subclass')

    def __len__(self):
        """Return the total number of elements in the tree."""
        raise NotImplementedError('must be implemented by subclass')

    # ---------- concrete methods implemented in this class ----------
    """
    is_root(self,p)는 position p에 해당하는 노드가 tree 객체에서의 root가 맞는지를 확인해주는 역할을 수행하며 이에 대해서 boolean value를 반환한다.
    
    :param p: position p 객체를 가리킨다.
    :return: tree 객체의 root의 position과 p position이 일치하는지에 대한 boolean value를 반환한다.
    """
    def is_root(self, p):
        """Return True if Position p represents the root of the tree."""
        return self.root() == p

    """
    is_leaf(self,p)는 position p에 해당하는 노드가 tree 객체에서의 leaf가 맞는지를 확인해준는 역할을 수행하며 이에 대해서 boolean value를 반환한다.
    
    :param p: position p 객체를 가리킨다.
    :return: position p에 해당하는 노드의 자식의 수가 0이 맞는지, 즉 position p에 해당하는 노드가 leaf가 맞는지에 대한 boolean value를 반환한다.
    """
    def is_leaf(self, p):
        """Return True if Position p does not have any children."""
        return self.num_children(p) == 0

    """
    is_empty(self)는 tree 객체가 empty한지에 대한 여부를 boolean value로 반환해주는 역할을 수행한다.
    
    :return: tree 객체 내의 요소 개수와 0을 비교하여 이에 대한 boolean value를 반환한다.
    """
    def is_empty(self):
        """Return True if the tree is empty."""
        return len(self) == 0

    """
    depth(self, p)는 position p에 해당하는 노드의 tree에서의 depth를 반환해주는 역할을 재귀적으로 수행한다. 첫 조건문 부분에서 if self.is_root(p)를 통해 base case를 만들고 else문 부분에서 recursive case(재귀호출 및 재귀호출 결과에 1을 더해주는)를 두어 그 역할에 따라 기능할 수 있다.
    
    :param p: position p 객체를 가리킨다.
    :return: position p에 해당하는 노드의 tree에서의 depth를 반환한다.
    """
    def depth(self, p):
        """Return the number of levels separating Position p from the root."""
        if self.is_root(p):
            return 0
        else:
            return 1 + self.depth(self.parent(p))

    """
    height(self, p)는 position p에 해당하는 노드를 root로 하는 subtree의 height을 반환해주는 역할을 재귀적으로 수행한다. 첫 조건문 부분에서 if self.is_leaf(p)를 통해 base case를 만들고 else문 부분에서 recursive case(재귀호출 및 재귀호출 결과에 1을 더해주는)를 두어 그 역할에 따라 기능할 수 있다. 구체적으로는, recursive case에서 p에 해당하는 노드의 자식 노드들에 대해 반복문을 두고 해당 자식 노드들 모두에 대해 재귀적으로 height을 구한 뒤 이에 대한 max 값에 1을 더해주는 방안을 사용한다.
    
    :param p: position p 객체를 가리킨다.
    :return: position p에 해당하는 노드를 루트로 하는 subtree의 height을 반환한다.
    """
    def _height(self, p):                                    # time is linear in size of subtree
        """Return the height of the subtree rooted at Position p."""
        if self.is_leaf(p):
            return 0
        else:
            return 1 + max(self._height(c) for c in self.children(p))

    """
    height(self, p=None)은 position p에 해당하는 노드를 루트 노드를 하는 subtree의 height을 반환하는 역할을 수행한다. p의 default value가 None으로 설정되어있으며 실제로 None value를 받거나 value를 받지 않을시 전체 tree의 height을 반환한다. 이 경우, p를 root 노드의 position으로 간주한다. 역할을 수행하는 과정 중에, return에서 self._height을 이용하므로 재귀가 일어난다.
    
    :param p: positon p 객체를 가리킨다. (default value는 None이다.)
    :return: p position에 해당하는 노드를 루트 노드로 하는 subtree의 height을 return한다.
    """
    def height(self, p=None):
        """Return the height of the subtree rooted at Position p.

        If p is None, return the height of the entire tree.
        """
        if p is None:
            p = self.root()
        return self._height(p)                # start _height2 recursion

    """
    __iter__(self)는 tree의 element들에 대한 iteration을 generate하는 역할을 수행한다. self.positions를 이용한 반복문을 통해 element들의 position을 알고 이 position에 해당하는 노드의 element를 yield하여 역할을 수행한다.
    
    :yield: tree내 노드들의 postion들 각각에 대한 element를 yield 한다.
    """
    def __iter__(self):
        """Generate an iteration of the tree's elements."""
        for p in self.positions():     # use same order as positions()
            yield p.element()          # but yield each element

    """
    positions(self)는 tree의 position들에 대한 iteration을 generate하는 역할을 수행한다. 이 역할의 수행은 self.preorder()를 통해 수행된다.
    
    :return: tree 객체 전체에 대한 preorder iteration을 반환한다.
    """
    def positions(self):
        """Generate an iteration of the tree's positions."""
        return self.preorder()         # return entire preorder iteration

    """
    preorder(self)는 tree 객체에 대한 position들에 대한 preorder iteration을 generate하는 역할을 수행한다. 이 역할을 수행하기 위해서 우선 tree가 empty인지 확인하기 위해서 if no self.is_empty()의 조건문을 통과하고(empty라면 None이 return될 것.) 그 뒤에 self._subtree_preorder에 root node의 position을 넣어주는 방안을 이용한 반복문을 통해서 position들을 yield한다.
    
    :return / yield: 만약 tree 객체가 empty라면 None을 반환, tree 객체가 empty가 아니라면 tree 객체의 position들 각각에 대해 yield한다.
    """
    def preorder(self):
        """Generate a preorder iteration of positions in the tree."""
        if not self.is_empty():
            for p in self._subtree_preorder(self.root()):    # start recursion
                yield p

    """
    _subtree_preorder(self,p)는 p position의 노드를 root node로 하는 subtree에 대해서 position들의 preorder iteration을 generate하는 역할을 재귀적으로 수행한다. 이를 자세히 들여다보자면, 우선 p가 position인 노드를 root로 하는 subtree에 대한 preorder iteration이므로 제일 먼저 p를 yield한다. 그 뒤에는 p position 노드의 children에 대한 반복문을 만들고 각 child position을 다시 루트로 하는 subtree에 대한 self._subtree_preorder(c)를 재귀적으로 수행하고 이에 대해 다시 반복문을 걸어서 결론적으로 other 부분에 해당하는 positon을 yield한다.
    
    :param p: subtree의 root 자리가 되는 노드의 position p 객체를 가리킨다.
    :yield: 제일 우선 루트 노드의 position을 yield하고 그 뒤로는 재귀적으로 그 자식들에 대한 _subtree_preorder를 사용하여 자식들의 position을 yield한다.
    """
    def _subtree_preorder(self, p):
        """Generate a preorder iteration of positions in subtree rooted at p."""
        yield p                       # visit p before its subtrees
        for c in self.children(p):                 # for each child c
            for other in self._subtree_preorder(c):              # do preorder of c's subtree
                yield other                                               # yielding each to our caller

    """
    postorder(self)는 tree 객체에 있는 노드들의 position들에 대해 postorder iteration을 generation하는 역할을 수행한다. 우선, if not self.is_empty()를 통해 tree가 empty한 지를 확인한다. tree가 empty한 경우 조건문 아래의 코드를 진행하지 못하기 때문에 None을 반환한다. tree가 empty하지 않은 경우에는 조건문 아래의 코드 진행이 가능하며, self._subtree_postorder에 root node의 position을 넣어주는 방안을 이용해서 이를 반복문에 넣어 tree 객체 전체에 대한 position들 각각을 postorder로 yield한다.
    
    :return / yield: tree가 empty인 경우에 None을 return, tree가 empty하지 않은 경우에 tree내 position들 각각을 postorder로 yield한다.
    """
    def postorder(self):
        """Generate a postorder iteration of positions in the tree."""
        if not self.is_empty():
            for p in self._subtree_postorder(self.root()):    # start recursion
                yield p

    """
    _subtree_postorder(self,p)는 p positon에 대한 노드를 루트 노드로 하는 subtree에서의 position들에 대해 postorder iteration을 generate한다. p position의 노드에 대한 자식들에 대한 반복문에서 자식 각각에 대해 재귀적으로 self._subtree_postorder(c)를 적용하고 이에 대한 반복문에서 other를 yield해주면 position p를 제외한 p를 루트로 하는 subtree의postorder iteration이 완성되고 마지막으로 p를 yield해주면 p를 루트로 하는 subtree에서 position들에 대한 postorder iteration이 완성된다.
    
    :yield: p position node를 루트로 하는 subtree의 position들 각각에 대해 postorder로 yield한다.
    """
    def _subtree_postorder(self, p):
        """Generate a postorder iteration of positions in subtree rooted at p."""
        for c in self.children(p):       # for each child c
            for other in self._subtree_postorder(c):  # do postorder of c's subtree
                yield other      # yielding each to our caller
        yield p             # visit p after its subtrees

    """
    levelorder(self) 메소드는 levelorder traversal의 순서로 tree 객체의 position을 yield한다. levelorder traversal은 tree의 node들을 level by level로, 각 level에서는 왼쪽에서 오른쪽으로 노드들을 방문하는 것을 말한다. 해당 메소드를 구현하기 위해서 queue를 이용한다.(여기선 q로 지정) 먼저 queue가 될 빈 리스트를 만들고 이 리스트에 root 노드를 append한다. 그 뒤에 queue에서 dequeue된, 즉 pop된 item들을 담을 빈 리스트를 만든다. (여기선, result라고 그 리스트를 담는 변수를 정했다.) 그 뒤에 queue의 첫 item을 부모로 지정한 뒤 이를 result에 넣고 그 자식을 queue에 넣고 다시 그 과정을 반복하고 이 과정을 통해 queue에는 맨 앞 노드가 하나씩 dequeue됨과 동시에 levelorder traversal 순서에 맞게 그 자식이 enqueue되기 때문에 최종적으로 result에 levelorder traversal 순서에 맞게 노드들이 append된다. 그 이후에는 for ele in result 반복문으로 result 리스트에 있는 노드들 각각에 대해서 그 position을 yield한다.
    이 메소드의 running time은 O(n)이다. (for문이 들어있는 while문의 경우 결국 tree에 들어있는 노드들이 levelorder traversal 순서에 맞게 리스트에 들어가도록 하는 것이고 pop을 진행하며 len(q) == 0이 될때까지 진행하게 되는 반복문이므로 총 O(n)이 소요되며 그 뒤 for ele in result 반복문 역시 result에 들어있는 노드들의 수, 즉 tree에 있는 노드들의 수에 맞추어 반복되기 때문에 O(n)이다.)
    
    :yield: levelorder traversal 순서에 맞추어 tree에 있는 노드들 각각의 position을 yield한다.
    """
    def levelorder(self):
        q = []
        q.append(self._validate(self._root))
        result = []
        while len(q) > 0:
            pr = q.pop(0)
            result.append(pr)
            for ch in pr._children:
                q.append(self._validate(self._make_position(ch)))
        for ele in result:
            yield self._make_position(ele)