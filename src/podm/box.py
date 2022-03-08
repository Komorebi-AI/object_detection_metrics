class Box:
    def __init__(self, xtl: float, ytl: float, xbr: float, ybr: float):
        """
                    0,0 ------> x (width)
             |
             |  (Left,Top)
             |      *_________
             |      |         |
                    |         |
             y      |_________|
          (height)            *
                        (Right,Bottom)

        Args:
            xtl: the X top-left coordinate of the bounding box.
            ytl: the Y top-left coordinate of the bounding box.
            xbr: the X bottom-right coordinate of the bounding box.
            ybr: the Y bottom-right coordinate of the bounding box.
        """
        assert xtl <= xbr, f'xtl < xbr: xtl:{xtl}, xbr:{xbr}'
        assert ytl <= ybr, f'ytl < ybr: ytl:{ytl}, xbr:{ybr}'

        self.xtl = xtl
        self.ytl = ytl
        self.xbr = xbr
        self.ybr = ybr

    @property
    def width(self) -> float:
        return self.xbr - self.xtl

    @property
    def height(self) -> float:
        return self.ybr - self.ytl

    @property
    def area(self) -> float:
        return (self.xbr - self.xtl) * (self.ybr - self.ytl)

    def __str__(self):
        return 'Box[xtl={},ytl={},xbr={},ybr={}]'.format(self.xtl, self.ytl, self.xbr, self.ybr)


def intersection_over_union(box1: 'Box', box2: 'Box') -> float:
    """
    Intersection Over Union (IOU) is measure based on Jaccard Index that evaluates the overlap between
    two bounding boxes.
    """
    # if boxes dont intersect
    if not is_intersecting(box1, box2):
        return 0
    intersection_area = intersection(box1, box2).area
    union = union_areas(box1, box2, intersection_area=intersection_area)
    # intersection over union
    iou = intersection_area / union
    assert iou >= 0, '{} = {} / {}, box1={}, box2={}'.format(iou, intersection, union, box1, box2)
    return iou


def is_intersecting(box1: 'Box', box2: 'Box') -> bool:
    if box1.xtl > box2.xbr:
        return False  # boxA is right of boxB
    if box2.xtl > box1.xbr:
        return False  # boxA is left of boxB
    if box1.ybr < box2.ytl:
        return False  # boxA is above boxB
    if box1.ytl > box2.ybr:
        return False  # boxA is below boxB
    return True


def union_areas(box1: 'Box', box2: 'Box', intersection_area: float = None) -> float:
    if intersection_area is None:
        intersection_area = intersection(box1, box2).area
    return box1.area + box2.area - intersection_area


def union(box1: 'Box', box2: 'Box'):
    xtl = min(box1.xtl, box2.xtl)
    ytl = min(box1.ytl, box2.ytl)
    xbr = max(box1.xbr, box2.xbr)
    ybr = max(box1.ybr, box2.ybr)
    return Box(xtl, ytl, xbr, ybr)


def intersection(box1: 'Box', box2: 'Box'):
    xtl = max(box1.xtl, box2.xtl)
    ytl = max(box1.ytl, box2.ytl)
    xbr = min(box1.xbr, box2.xbr)
    ybr = min(box1.ybr, box2.ybr)
    return Box(xtl, ytl, xbr, ybr)
