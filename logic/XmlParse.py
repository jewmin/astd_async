try:
    import xml.etree.cElementTree as Et
except ImportError:
    import xml.etree.ElementTree as Et


def _ParseNode(node: Et.Element) -> dict:
    tree = {}

    # Save childrens
    for child in node:
        ctag = child.tag
        ctext = child.text.strip() if child.text is not None else ''
        ctree = _ParseNode(child)

        if not ctree:
            cdict = _MakeDict(ctag, ctext)
        else:
            cdict = _MakeDict(ctag, ctree)

        if ctag not in tree:  # First time found
            tree.update(cdict)
            continue

        atree = tree[ctag]
        if not isinstance(atree, list):
            tree[ctag] = [atree]  # Multi entries, change to list

        if not ctree:
            tree[ctag].append(ctext)
        else:
            tree[ctag].append(ctree)

    return tree


def _MakeDict(tag: str, value: str):
    """Generate a new dict with tag and value"""
    return {tag: value}


def Parse(xml: str) -> dict:
    """Parse xml string to python dict"""
    el = Et.fromstring(xml)

    ctree = _ParseNode(el)

    if not ctree:
        cdict = _MakeDict(el.tag, el.text)
    else:
        cdict = _MakeDict(el.tag, ctree)

    return cdict
