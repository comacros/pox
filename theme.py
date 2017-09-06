import PyOrigin as po


def _potree(treenode):
    if not isinstance(treenode, po.CPyTreeNode):
        raise TypeError('Input must be a PyOrigin.CPyTreeNode')

    kv = {}
    if(len(treenode.Children())):
        for subnode in treenode.Children():
            kv[subnode.Name] = _potree(subnode)
    else:
        return treenode.GetStrValue()

    return kv


def _potreeFromPath(treenode, paths):
    if not isinstance(treenode, po.CPyTreeNode):
        raise TypeError('First input must be a PyOrigin.CPyTreeNode')
    if not isinstance(paths, list):
        raise TypeError('Second input must be a list')
    node = treenode
    level = 0
    for path in paths:
        for sub in node:
            if sub.Name == path:
                node = sub
                level += 1
                break
    return node if level == len(paths) else None


class TreeNode(dict):
    def __init__(self, *args, **kwargs):
        if len(args) != 1 or not isinstance(args[0], dict):
            return TreeNode(dict())
        for k, v in args[0].items():
            self.update({k: TreeNode(v) if isinstance(v, dict) else v})

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, attr, val):
        self.update({attr: val})


def _poTreeNodeToTheme(treenode, theme):
    if not isinstance(treenode, TreeNode) or not isinstance(theme, po.CPyTreeNode):
        raise TypeError('The input data types should be pox.theme.TreeNode and PyOrigin.CPyTreeNode respectively')
    for subTheme in theme.Children():
        name = subTheme.Name
        if name in treenode:
            val = treenode[name]
            if subTheme.Children().GetCount():
                if isinstance(val, TreeNode):
                    _poTreeNodeToTheme(val, subTheme)
            else:
                if isinstance(val, int):
                    subTheme.SetIntValue(val)
                elif isinstance(val, float):
                    subTheme.SetDoubleValue(val)
                elif isinstance(val, str) and val != subTheme.GetStrValue():
                    subTheme.SetStrValue(val)


class Theme:
    def __init__(self, poobj):
        if not isinstance(poobj, po.CPyOriginObject):
            raise TypeError('Input must be a PyOrigin.CPyOriginObject.')
        self.theme = poobj.GetTheme()
        self.obj = poobj
        self.val = TreeNode(_potree(self.theme), obj = self.obj)

    @property
    def Root(self):
        return self.val

    @Root.setter
    def Root(self, val):
    	if isinstance(val, dict):
    		self.val = TreeNode(val)
    		self.apply()
    	elif isinstance(val, TreeNode):
    		self.val = val
    		self.apply()

    def __str__(self):
        return self.Root.__str__()

    def __getattr__(self, attr):
        return self.Root.get(attr)

    def apply(self):
        _poTreeNodeToTheme(self.Root, self.theme)
        self.obj.SetTheme(self.theme)


if __name__ == '__main__':
    pass