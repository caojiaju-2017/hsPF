/**工具类*/
var Util = (function () {
    /**根据点击事件，获取鼠标位置*/
    this.getMousePosition = function (e) {
        var x = getX(e);
        var y = getY(e);
        return x + ',' + y;
    };

    this.isBlank = function (obj) {
        if (typeof(obj) == "undefined" || obj == null
            || (typeof(obj) != "object"
            && (obj + "").replace(/\s*/g, "") == "")) {
            return true;
        }
        return false;
    };

    /**根据点击事件，获取鼠标位置*/
    this.getMousePositionObj = function (e) {
        var x = getX(e);
        var y = getY(e);
        return {x: x, y: y};
    };

    function getX(e) {
        e = e || window.event;
        return e.pageX || e.clientX + document.body.scroolLeft;
    }

    function getY(e) {
        e = e || window.event;
        return e.pageY || e.clientY + document.boyd.scrollTop;
    }

    /**圆角阴影边框*/
    this.shadowBorder = function (selector, val1, val2, val3, radius, color) {
        var tgtEl = $(selector);
        var behaviorUrl = path + '/js/app/shadow/PIE.htc';
        var css = [];
        var shadow = val1 + "px " + val2 + "px " + val3 + "px " + color + ";";

        css.push("-webkit-box-shadow:" + shadow);
        css.push("-moz-box-shadow:" + shadow);
        css.push("-webkit-border-radius:" + radius + "px;");
        css.push("-moz-border-radius:" + radius + "px;");
        css.push("background:#FFFFFF;");
        css.push('border:1px solid #CACACA;');
        css.push("box-shadow:" + shadow);
        css.push("border-radius:" + radius + "px;");
        css.push("behavior:url(" + behaviorUrl + ");");

        var style = "";

        if (!Util.isBlank(tgtEl[0].style.cssText)) {
            style = css.join(tgtEl[0].style.cssText + ';');
        } else {
            style = css.join(" ");
        }

        tgtEl[0].style.cssText = style;

        if (tgtEl[0].addBehavior) {
            tgtEl[0].addBehavior(behaviorUrl);
        }
    };

    return this;
})();

/**
 * flipsnap.js
 *
 * @version  0.5.3
 * @url http://pxgrid.github.com/js-flipsnap/
 *
 * Copyright 2011 PixelGrid, Inc.
 * Licensed under the MIT License:
 * http://www.opensource.org/licenses/mit-license.php
 */

(function (window, document, undefined) {

    var div = document.createElement('div');
    var prefix = ['webkit', 'moz', 'o', 'ms'];
    var saveProp = {};
    var support = Flipsnap.support = {};
    var gestureStart = false;

    support.transform3d = hasProp([
        'perspectiveProperty',
        'WebkitPerspective',
        'MozPerspective',
        'OPerspective',
        'msPerspective'
    ]);

    support.transform = hasProp([
        'transformProperty',
        'WebkitTransform',
        'MozTransform',
        'OTransform',
        'msTransform'
    ]);

    support.transition = hasProp([
        'transitionProperty',
        'WebkitTransitionProperty',
        'MozTransitionProperty',
        'OTransitionProperty',
        'msTransitionProperty'
    ]);

    support.addEventListener = 'addEventListener' in window;
    support.mspointer = window.navigator.msPointerEnabled;

    support.cssAnimation = (support.transform3d || support.transform)
        && support.transition;

    var eventTypes = ['touch', 'mouse', 'pointer'];
    var events = {
        start: {
            touch: 'touchstart',
            mouse: 'mousedown',
            pointer: 'MSPointerDown'
        },
        move: {
            touch: 'touchmove',
            mouse: 'mousemove',
            pointer: 'MSPointerMove'
        },
        end: {
            touch: 'touchend',
            mouse: 'mouseup',
            pointer: 'MSPointerUp'
        }
    };

    if (support.addEventListener) {

        document.addEventListener('gesturestart', function () {
            gestureStart = true;
        });

        document.addEventListener('gestureend', function () {
            gestureStart = false;
        });
    }

    function Flipsnap(element, opts) {
        return (this instanceof Flipsnap)
            ? this.init(element, opts)
            : new Flipsnap(element, opts);
    }

    Flipsnap.prototype.init = function (element, opts) {
        var self = this;

        // set element
        self.element = element;
        if (typeof element === 'string') {
            self.element = document.querySelector(element);
        }

        if (!self.element) {
            throw new Error('element not found');
        }

        if (support.mspointer) {
            self.element.style.msTouchAction = 'none';
        }

        // set opts
        opts = opts || {};
        self.distance = opts.distance;
        self.maxPoint = opts.maxPoint;
        self.disableTouch = (opts.disableTouch === undefined)
            ? false : opts.disableTouch;
        self.disable3d = (opts.disable3d === undefined)
            ? false : opts.disable3d;
        self.transitionDuration = (opts.transitionDuration === undefined)
            ? '350ms' : opts.transitionDuration + 'ms';

        // set property
        self.currentPoint = 0;
        self.currentX = 0;
        self.animation = false;
        self.use3d = support.transform3d;
        if (self.disable3d === true) {
            self.use3d = false;
        }

        // set default style
        if (support.cssAnimation) {
            self._setStyle({
                transitionProperty: getCSSVal('transform'),
                transitionTimingFunction: 'cubic-bezier(0,0,0.25,1)',
                transitionDuration: '0ms',
                transform: self._getTranslate(0)
            });
        }
        else {
            self._setStyle({
                position: 'relative',
                left: '0px'
            });
        }

        // initilize
        self.refresh();

        $.each(eventTypes, function (i, type) {
            $(self.element).bind(events.start[type], self, self.handleEvent);
        });

        return self;
    };

    Flipsnap.prototype.handleEvent = function (event) {
        var self = event.data;
        switch (event.type) {
            case events.start.touch:
            case events.start.mouse:
            case events.start.pointer:
                self._touchStart(event);
                break;
            case events.move.touch:
            case events.move.mouse:
            case events.move.pointer:
                self._touchMove(event);
                break;
            case events.end.touch:
            case events.end.mouse:
            case events.end.pointer:
                self._touchEnd(event);
                break;
            case 'click':
                self._click(event);
                break;
        }
    };

    Flipsnap.prototype.refresh = function () {
        var self = this;

        // setting max point
        self._maxPoint = (self.maxPoint === undefined) ? (function () {
            var childNodes = self.element.childNodes,
                itemLength = 0,
                i = 0,
                len = childNodes.length,
                node;
            for (; i < len; i++) {
                node = childNodes[i];
                if (node.nodeType === 1) {
                    itemLength++;
                }
            }
            if (itemLength > 0) {
                itemLength--;
            }

            return itemLength;
        })() : self.maxPoint;

        // setting distance
        self._distance = (self.distance === undefined)
            ? self.element.scrollWidth / (self._maxPoint + 1)
            : self.distance;

        // setting maxX
        self._maxX = -self._distance * self._maxPoint;

        self.moveToPoint();
    };

    Flipsnap.prototype.hasNext = function () {
        var self = this;

        return self.currentPoint < self._maxPoint;
    };

    Flipsnap.prototype.hasPrev = function () {
        var self = this;

        return self.currentPoint > 0;
    };

    Flipsnap.prototype.toNext = function (transitionDuration) {
        var self = this;

        if (!self.hasNext()) {
            return;
        }

        self.moveToPoint(self.currentPoint + 1, transitionDuration);
    };

    Flipsnap.prototype.toPrev = function (transitionDuration) {
        var self = this;

        if (!self.hasPrev()) {
            return;
        }

        self.moveToPoint(self.currentPoint - 1, transitionDuration);
    };

    Flipsnap.prototype.moveToPoint = function (point, transitionDuration) {
        var self = this;

        transitionDuration = transitionDuration === undefined
            ? self.transitionDuration : transitionDuration + 'ms';

        var beforePoint = self.currentPoint;

        // not called from `refresh()`
        if (point === undefined) {
            point = self.currentPoint;
        }

        if (point < 0) {
            self.currentPoint = 0;
        }
        else if (point > self._maxPoint) {
            self.currentPoint = self._maxPoint;
        }
        else {
            self.currentPoint = parseInt(point, 10);
        }

        if (support.cssAnimation) {
            self._setStyle({ transitionDuration: transitionDuration });
        }
        else {
            self.animation = true;
        }
        self._setX(-self.currentPoint * self._distance, transitionDuration);

        if (beforePoint !== self.currentPoint) { // is move?
            // `fsmoveend` is deprecated
            // `fspointmove` is recommend.
            self._triggerEvent('fsmoveend', true, false,
                {newPoint: self.currentPoint});
            self._triggerEvent('fspointmove', true, false);
        }
    };

    Flipsnap.prototype._setX = function (x, transitionDuration) {
        var self = this;

        self.currentX = x;
        if (support.cssAnimation) {
            self.element.style[ saveProp.transform ] = self._getTranslate(x);
        }
        else {
            if (self.animation) {
                self._animate(x, transitionDuration
                    || self.transitionDuration);
            }
            else {
                self.element.style.left = x + 'px';
            }
        }
    };

    Flipsnap.prototype._touchStart = function (event) {

        var self = event.data;

        if (self.disableTouch || self._eventType || gestureStart) {
            return;
        }

        some(eventTypes, function (type) {
            if (event.type === events.start[type]) {
                self._eventType = type;
                return true;
            }
        });

        $(self.element).bind(events.move[self._eventType],
            self, self.handleEvent);
        $(document).bind(events.end[self._eventType], self, self.handleEvent);

        if (self._eventType === 'mouse') {
            event.preventDefault();
        }

        if (support.cssAnimation) {
            self._setStyle({ transitionDuration: '0ms' });
        }
        else {
            self.animation = false;
        }
        self.scrolling = true;
        self.moveReady = false;
        self.startPageX = getPage(event, 'pageX');
        self.startPageY = getPage(event, 'pageY');
        self.basePageX = self.startPageX;
        self.directionX = 0;
        self.startTime = event.timeStamp;
        self._triggerEvent('fstouchstart', true, false);
    };

    Flipsnap.prototype._touchMove = function (event) {
        var self = this;


        if (!self.scrolling || gestureStart) {
            return;
        }

        var pageX = getPage(event, 'pageX'),
            pageY = getPage(event, 'pageY'),
            distX,
            newX,
            deltaX,
            deltaY;

        if (self.moveReady) {
            event.preventDefault();
            event.stopPropagation();

            distX = pageX - self.basePageX;
            newX = self.currentX + distX;
            if (newX >= 0 || newX < self._maxX) {
                newX = Math.round(self.currentX + distX / 3);
            }

            // When distX is 0, use one previous value.
            // For android firefox. When touchend fired, touchmove also
            // fired and distX is certainly set to 0.
            self.directionX =
                distX === 0 ? self.directionX :
                    distX > 0 ? -1 : 1;

            // if they prevent us then stop it
            var isPrevent = !self._triggerEvent('fstouchmove', true, true, {
                delta: distX,
                direction: self.directionX
            });

            if (isPrevent) {
                self._touchAfter({
                    moved: false,
                    originalPoint: self.currentPoint,
                    newPoint: self.currentPoint,
                    cancelled: true
                });
            } else {
                self._setX(newX);
            }
        }
        else {
            deltaX = Math.abs(pageX - self.startPageX);
            deltaY = Math.abs(pageY - self.startPageY);
            if (deltaX > 5) {
                event.preventDefault();
                event.stopPropagation();
                self.moveReady = true;
                $(self.element).bind('click', self, self.handleEvent);
            }
            else if (deltaY > 5) {
                self.scrolling = false;
            }
        }

        self.basePageX = pageX;
    };

    Flipsnap.prototype._touchEnd = function (event) {
        var self = this;

        self._eventType = 'touch';
        $(self.element).unbind(events.move[self._eventType],
            self, self.handleEvent);
        $(document).unbind(events.end[self._eventType], self, self.handleEvent);

        self._eventType = null;

        if (!self.scrolling) {
            return;
        }

        var newPoint = -self.currentX / self._distance;
        newPoint =
            (self.directionX > 0) ? Math.ceil(newPoint) :
                (self.directionX < 0) ? Math.floor(newPoint) :
                    Math.round(newPoint);

        if (newPoint < 0) {
            newPoint = 0;
        }
        else if (newPoint > self._maxPoint) {
            newPoint = self._maxPoint;
        }

        self._touchAfter({
            moved: newPoint !== self.currentPoint,
            originalPoint: self.currentPoint,
            newPoint: newPoint,
            cancelled: false
        });

        self.moveToPoint(newPoint);
    };

    Flipsnap.prototype._click = function (event) {
        var self = this;

        event.stopPropagation();
        event.preventDefault();
    };

    Flipsnap.prototype._touchAfter = function (params) {
        var self = this;

        self.scrolling = false;
        self.moveReady = false;

        setTimeout(function () {
            $(self.element).unbind('click', self, self.handleEvent);
        }, 200);
        self._triggerEvent('fstouchend', true, false, params);
    };

    Flipsnap.prototype._setStyle = function (styles) {
        var self = this;
        var style = self.element.style;

        for (var prop in styles) {
            setStyle(style, prop, styles[prop]);
        }
    };

    Flipsnap.prototype._animate = function (x, transitionDuration) {
        var self = this;

        var elem = self.element;
        var begin = +new Date();
        var from = parseInt(elem.style.left, 10);
        var to = x;
        var duration = parseInt(transitionDuration, 10);
        var easing = function (time, duration) {
            return -(time /= duration) * (time - 2);
        };
        var timer = setInterval(function () {
            var time = new Date() - begin;
            var pos, now;
            if (time > duration) {
                clearInterval(timer);
                now = to;
            }
            else {
                pos = easing(time, duration);
                now = pos * (to - from) + from;
            }
            elem.style.left = now + "px";
        }, 10);
    };

    Flipsnap.prototype.destroy = function () {
        var self = this;

        $.each(eventTypes, function (i, type) {
            $(self.element).unbind(events.start[type], self, self.handleEvent);
        });
    };

    Flipsnap.prototype._getTranslate = function (x) {
        var self = this;

        return self.use3d
            ? 'translate3d(' + x + 'px, 0, 0)'
            : 'translate(' + x + 'px, 0)';
    };

    Flipsnap.prototype._triggerEvent =
        function (type, bubbles, cancelable, data) {
            var self = this;

            if (data) {
                for (var d in data) {
                    self[d] = data[d];
                }
            }

            return $(self.element).trigger(type, self);
        };

    function getPage(event, page) {
        var originalEvent = event.originalEvent || event;
        return originalEvent.changedTouches
            ? originalEvent.changedTouches[0][page]
            : originalEvent[page] || event[page];
    }

    function hasProp(props) {
        return some(props, function (prop) {
            return div.style[ prop ] !== undefined;
        });
    }

    function setStyle(style, prop, val) {
        var _saveProp = saveProp[ prop ];
        if (_saveProp) {
            style[ _saveProp ] = val;
        }
        else if (style[ prop ] !== undefined) {
            saveProp[ prop ] = prop;
            style[ prop ] = val;
        }
        else {
            some(prefix, function (_prefix) {
                var _prop = ucFirst(_prefix) + ucFirst(prop);
                if (style[ _prop ] !== undefined) {
                    saveProp[ prop ] = _prop;
                    style[ _prop ] = val;
                    return true;
                }
            });
        }
    }

    function getCSSVal(prop) {
        if (div.style[ prop ] !== undefined) {
            return prop;
        }
        else {
            var ret;
            some(prefix, function (_prefix) {
                var _prop = ucFirst(_prefix) + ucFirst(prop);
                if (div.style[ _prop ] !== undefined) {
                    ret = '-' + _prefix + '-' + prop;
                    return true;
                }
            });
            return ret;
        }
    }

    function ucFirst(str) {
        return str.charAt(0).toUpperCase() + str.substr(1);
    }

    function some(ary, callback) {
        for (var i = 0, len = ary.length; i < len; i++) {
            if (callback(ary[i], i)) {
                return true;
            }
        }
        return false;
    }

    window.Flipsnap = Flipsnap;

})(window, window.document);

/**
 *
 * @param select 选择器 如：#id，.className等
 * @param opts 配置信息
 * @returns {*}
 * @constructor
 */
function BasePanel(select, opts) {
    var $this = this;
    $this.$container = $(select);

    if ($this.$container.length == 0) {
        throw new Error('为找到指定的元素[' + select + ']');
        return;
    }

    //基础默认配置
    var defaultBaseCfg = {
        /**面板显示的元素个数*/
        count: 0,
        /**面板可视范围内显示的元素个数，如果展开后，
         * 则是disItem = disItem * expanRow*/
        disItem: 0,
        /**展示时显示的个数*/
        disItemExpan: 0,
        /**显示面板宽度*/
        width: 0,
        /**面板里需要承载的html内容*/
        contentHtml: [],
        /**是否显示展开按钮*/
        isExpan: false,
        /**是否自动展开*/
        isAutoExpan: false,
        /**展开后显示的行数*/
        expanRows: 0,
        /**箭头位置：top：顶部；middle：中间*/
        arrowAlign: 'middle',
        /**面板移动完成后事件*/
        onmoveend: null,
        /**状态*/
        expanStatus: false,
        /**页数*/
        pageSize: 0,
        /**展开页数*/
        pageSizeExpan: 0,
        /**每个图片宽度*/
        itemWidth: 0,
        /**展开时每个图片宽度*/
        itemWidthExpan: 0,
        /**鼠标点击事件*/
        itemClick: null,
        itemMarginTop: 9,
        /**面板展开事件*/
        expanEvent: null,
        /**顶部箭头样式*/
        topArrowCss: {'margin-right': 20},
        /***底部页码样式,不包含第一个元素*/
        pageCss: {'margin-left': 5},
        /***底部页码样式,仅指第一个元素*/
        pageFirstCss: {}
    };

    $this.opts = opts;

    //基础配置
    $this.baseCfg = {};

    //初始化页码控件
    $this.page = new Page($this);

    init(defaultBaseCfg, opts);

    /**
     * 初始化
     */
    function init(defaultBaseCfg, opts) {
        initBaseCfg(defaultBaseCfg, opts);

        appendHtml();

        appendItems();

        //设置样式
        setStyle();

        $this.page.init();

        //从原控件中继承方法
        extendMethods();

        //事件处理
        addEventHandler();
    }

    /**
     * 设置样式
     */
    function setStyle() {

        $this.$container.addClass('rightBot');

        var $tempFlipsnap = $('.flipsnap', $this.$container);
        //设置总宽度
        $tempFlipsnap.css({
            'width': $this.baseCfg.count * $this.baseCfg.itemWidth
        });

        $('.flipsnapContainer div.focus', $this.$container).css({
            width: $this.baseCfg.width -
                ($this.baseCfg.arrowAlign == 'middle' ? 46:
                    ($this.baseCfg.arrowAlign == 'none' ? 0 : 10))
        });

        $('.flipsnapContainer', $this.$container).css({
            width: $this.baseCfg.width
        });

        //单个图片显示区域大小
        $tempFlipsnap.children().css({
            width: ($this.baseCfg.isAutoExpan ?
                $this.baseCfg.itemWidthExpan :
                $this.baseCfg.itemWidth)
        });

        //在箭头居中的时候，需要微调左边距
        if ($this.baseCfg.isExpan && $this.baseCfg.arrowAlign == 'top') {
            $('.flipsnapContainer a.pickdown', $this.$container).css({
                right: -10
            });
        }
    }

    /**
     * 初始化基础配置
     * @returns {{}}
     */
    function initBaseCfg(_defaultBaseCfg, _opts) {

        $this.baseCfg =
            $.extend(_defaultBaseCfg,
                typeof(opts) == 'undefined' ? _defaultBaseCfg : opts);

        if ($this.baseCfg.isAutoExpan) {
            $this.baseCfg.expanStatus = true;
        }

        $this.baseCfg.contentHtml = _opts.contentHtml;

        $this.baseCfg.topArrowCss =
            $.extend($this.baseCfg.topArrowCss,
                typeof(_opts.topArrowCss) == 'undefined'
                    ? $this.baseCfg.topArrowCss
                    : _opts.topArrowCss);

        $this.baseCfg.pageCss =
            $.extend($this.baseCfg.pageCss,
                typeof(_opts.pageCss) == 'undefined'
                    ? $this.baseCfg.pageCss
                    : _opts.pageCss);

        if (_opts.pageFirstCss != null) {
            $this.baseCfg.pageFirstCss = _opts.pageFirstCss;
        }

        $this.baseCfg.count = _opts.contentHtml.length;
        $this.baseCfg.width = _opts.width || $this.$container.width();
        //每个图片宽度,44考虑左右箭头（17*2）及左箭头的right=10，共44
        var width = ($this.baseCfg.width -
            ($this.baseCfg.arrowAlign == 'middle' ? 44 :
                ($this.baseCfg.arrowAlign == 'none' ? 0 : 10)));

        if(_opts.itemWidth){
            $this.baseCfg.itemWidth = _opts.itemWidth + 5;
        }else{
            $this.baseCfg.itemWidth = Math.ceil(width / _opts.disItem);
        }

        $this.baseCfg.disItem = Math.floor(width / $this.baseCfg.itemWidth);

        $this.baseCfg.itemWidth = width / $this.baseCfg.disItem;

        //总页数
        $this.baseCfg.pageSize =
            Math.ceil($this.baseCfg.count / $this.baseCfg.disItem);

        //每次移动个数
        $this.baseCfg.distance =
            $this.baseCfg.itemWidth * $this.baseCfg.disItem;

        //页数，从0开始
        $this.baseCfg.pageNo = $this.baseCfg.pageSize - 1;

        //展开时每个图片宽度
        $this.baseCfg.itemWidthExpan = width;

        //展示时显示的个数
        $this.baseCfg.disItemExpan =
            ($this.baseCfg.expanRows * $this.baseCfg.disItem);

        //展开页数
        $this.baseCfg.pageSizeExpan =
            Math.ceil($this.baseCfg.count / $this.baseCfg.disItemExpan);

    }

    /**
     * 事件处理
     */
    function addEventHandler() {
        //移动完成后事件
        $($this.flipsnap.element).bind('fsmoveend', function (ev, data) {
            if ($this.baseCfg.onmoveend) {
                $this.baseCfg.onmoveend.call(this, data.newPoint + 1);
            }

            $this.page.setPageNoClass(data.newPoint);
        });

        expanHandler();
    }

    /**
     * 从原控件中基础方法
     */
    function extendMethods() {
        $.extend($this, {}, $this.flipsnap);
    }

    /**
     * 初始化原生控件
     */
    function initNativeCtrl(pageSize, width) {

        pageSize =
            pageSize || ($this.baseCfg.expanStatus ?
                $this.baseCfg.pageSizeExpan - 1 : $this.baseCfg.pageNo - 1);

        pageSize = (pageSize <= 0 ? 0 : pageSize);


        width =
            width || ($this.baseCfg.expanStatus ?
                $this.baseCfg.itemWidthExpan : $this.baseCfg.distance);

        if ($this.flipsnap) {
            $this.flipsnap.maxPoint = pageSize;
            $this.flipsnap.distance = width;
            $this.flipsnap.refresh();
        } else {
            $this.flipsnap = Flipsnap($('div.flipsnap', $this.$container)[0], {
                distance: width,
                maxPoint: pageSize
            });
        }

    }

    function appendHtml() {
        //先清空，避免多次调用
        $this.$container.empty();

        var warpHtml =
            '<div class="flipsnapContainer">' +
                '    <div class="arrowCtrlTop" style="display: none;"></div>' +
                '    <div class="focus">' +
                '       <div class="flipsnap">' +
                '       </div>' +
                '    </div>' +
                '    <div class="arrowCtrlMiddle" ' +
                'style="display: none;"></div>' +
                getExpanHtml() +
                '</div>' +
                '<div class="pageNo"></div>';

        $this.$container.append(warpHtml);

    }

    /**
     * 添加外部元素
     */
    function appendItems() {
        var baseCfg = $this.baseCfg;

        var $flipsnap = $('div.flipsnap', $this.$container);
        $flipsnap.empty();

        var pageSize = baseCfg.pageSize;

        var width = baseCfg.distance;

        var idx = 0;

        var clickSelector = "div.item";

        if (!baseCfg.expanStatus) {

            var html = "";

            for (var i = 0; i < baseCfg.contentHtml.length; i++) {
                var n = baseCfg.contentHtml[i];

                html += '<div class="item" ' +
                    'idx="' + (idx++) + '">' + n + '</div>';
            }

            $flipsnap.append(html).find('div.item')
                .css({width: baseCfg.itemWidth});
        } else {

            var html = "";

            pageSize = baseCfg.pageSizeExpan;

            clickSelector = "div.itemSmall";

            for (var i = 0; i < pageSize; i++) {
                var start = i * baseCfg.disItemExpan;
                var end = (start + baseCfg.disItemExpan);

                if (end >= baseCfg.contentHtml.length) {
                    end = baseCfg.contentHtml.length;
                }

                var htmlPage = '<div class="item">';

                for (var j = start; j < end; j++) {
                    htmlPage +=
                        '<div class="itemSmall" idx="' + (idx++) + '">' +
                            baseCfg.contentHtml[j] +
                            '</div>';
                }

                htmlPage += '</div>';

                html += htmlPage;
            }

            $flipsnap.append(html)
                .children().css({
                    width: baseCfg.itemWidthExpan
                })
                .children('div.itemSmall').css({
                    width: baseCfg.itemWidth
                    //"margin-top": baseCfg.itemMarginTop
                });

            width = baseCfg.itemWidthExpan;
        }

        $(clickSelector, $this.$container).mousedown(function (e) {
            $(this).attr('pos', '');
            $(this).attr('pos', Util.getMousePosition(e));
        }).mouseup(function (e) {

                if ($(this).attr('pos') != Util.getMousePosition(e)) {
                    return;
                }

                $(this).attr('pos', '');

                var idx = $(this).attr('idx');
                var item = baseCfg.contentHtml[idx];

                if (baseCfg.itemClick) {
                    baseCfg.itemClick.call(this, idx, $(e.target));
                }
            });

        initNativeCtrl(pageSize - 1, width);

        $this.page.initPageNoCtrl(pageSize);
        $this.page.initArrowsCtrl();
        $this.page.setPageNoClass(0);
    }


    function getExpanHtml() {

        $('div.flipsnap', $this.$container).empty();
        var html = "";
        if (opts.isExpan) {
            var className = (opts.isAutoExpan ? ' pickup' : '');
            html = '<a class="pickdown' + className + '" ' +
                ' title="点击展开/收拢"></a>';
        }

        return html;
    }


    /**
     * 展开处理
     */
    function expanHandler() {
        var baseCfg = $this.baseCfg;

        $('.flipsnapContainer a.pickdown', $this.$container)
            .click(function () {
                baseCfg.expanStatus = !baseCfg.expanStatus;
                appendItems();
                $this.flipsnap.moveToPoint(0);

                $(this).toggleClass('pickup');

                $("html,body").animate({scrollTop: $(this).offset().top}, 500);

                if (baseCfg.expanEvent) {
                    baseCfg.expanEvent
                        .call(this, baseCfg.expanStatus);
                }

            });
    }

    /**
     * 重新设置数据
     * @param contentHtml array
     */
    $this.resetContentHtml = function (contentHtml) {
        //基础配置
        initBaseCfg($this.baseCfg, {contentHtml: contentHtml});
        if ($this.baseCfg.expanStatus) {
            $this.baseCfg.expanStatus = !$this.baseCfg.expanStatus;
            $('.flipsnapContainer a.pickdown', $this.$container)
                .trigger('click');
        } else {
            appendItems();
            $this.flipsnap.moveToPoint(0);
        }
    };

    /**
     * 控件大小变化事件
     */
    $this.resize = function () {
        //基础配置
        $this.flipsnap = null;
        $this.opts.width = $this.$container.width();
        init($this.baseCfg, $this.opts);
    };

    return $this;

}

/**
 * 翻页对象, 包含底部分页圆圈按钮、及左右箭头翻页
 * @param basePanel 面板对象
 * @returns {*}
 * @constructor
 */
function Page(basePanel) {
    var $pageThis = this;
    //面板对象
    var $this = basePanel;

    var pageNoDivSelector = 'div.pageNo';
    var pageNoSelector = pageNoDivSelector + ' span';
    /**
     * 初始化页码控件
     */
    $pageThis.initPageNoCtrl = function (pageSize) {
        var pageHtml = '';

        for (var i = 0; i < pageSize; i++) {
            pageHtml += '<span val="' + i + '"></span>';
        }

        $(pageNoDivSelector, $this.$container).empty()
            .append(pageHtml)
            //第一个分页页码样式
            .children(':eq(0)').css($this.baseCfg.pageFirstCss).end()
            //除第一个分页页码样式
            .children(':gt(0)').css($this.baseCfg.pageCss).end()
            //页码单击事件
            .children()
            .click(function () {
                $this.flipsnap.moveToPoint($(this).attr('val'));
            });
    };

    $pageThis.initArrowsCtrl = function () {

        var left = "";
        /**
         * 初始化左右箭头控件
         */
        var right = "";

        $('div.arrowCtrlMiddle,div.arrowCtrlTop', $this.$container).empty();

        if ($this.baseCfg.arrowAlign == 'top') {
            left = "<ul class='pageTopArrow'>" +
                "<li class='next'></li>" +
                "<li class='pre'></li>" +
                "</ul>";

            $('div.arrowCtrlTop', $this.$container)
                .show()
                .append(left)
                .end()
                .find('ul.pageTopArrow')
                .css($this.baseCfg.topArrowCss);

        } else if ($this.baseCfg.arrowAlign == 'middle') {
            left = '<div class="pre pageArrow" style="opacity: 1;"></div>';
            right = '<div class="next pageArrow" style="opacity: 1;"></div>';
            $('div.arrowCtrlMiddle', $this.$container)
                .show().replaceWith(right);
            $('div.arrowCtrlTop', $this.$container).show().replaceWith(left);

            var height = $('div.focus', $this.$container).height();
            $('div.pageArrow', $this.$container).css({height: height});
        }

        //添加点击事件
        $('.pre', $this.$container).unbind('click').click(function () {
            $this.flipsnap.toPrev();
        });

        $('.next', $this.$container).unbind('click').click(function () {
            $this.flipsnap.toNext();
        });
    };

    /**
     * 翻页时，设置页码样式
     * @param pageNo 页码，从 0 开始
     */
    $pageThis.setPageNoClass = function (pageNo) {
        $(pageNoSelector, $this.$container)
            .removeClass('on')
            .eq(pageNo).addClass('on');

    };

    /**
     * 初始化分页控件（页码+箭头分页）
     */
    $pageThis.init = function () {
        this.initArrowsCtrl();
    };

    return $pageThis;

}


/**
 * 图片选择列表
 * @param selector 选择器 #id,.classname.....
 * @param opts 配置项
 * @constructor
 */
function SelectImgPanel(selector, opts) {
    //当前控件对象
    var $this = this;
    //当前控件容器
    $this.$container = $(selector);

    if ($this.$container.length == 0) {
        throw new Error('为找到指定的元素[' + selector + ']');
        return;
    }

    //强制给当前容器添加样式，并清空内容
    $this.$container.addClass('selImg');

    var defaultCfg = {
        /**默认的图片*/
        defalutImgUrl: path + "/images/app/flipsnap/default.png",
        /**每个item宽度*/
        itemWidth: 155,
        /**每个item高度*/
        itemHeight: 61,
        /**可供选择的图片数据*/
        contentHtml: [],
        /**弹窗宽度*/
        showWidth: 620,
        /**弹窗父容器ID*/
        imgListId: (new Date().getTime() +
            Math.floor(Math.random() * 100000) + "imgListId"),
        /**弹窗容器ID*/
        imgCtrlId: (new Date().getTime() +
            Math.floor(Math.random() * 100000) + "imgCtrlId"),
        imgListCtrl: null,
        isReSetData: false,
        /**组装html*/
        getHtmlFormat: function (item, i) {
            var html = '<div class="bisItem">' +
                '<span class="container">' +
                '<img src="' + item.customImg + '">' +
                '</span>' +
                '<a class="sName">' + item.customName + '</a>' +
                '<div style="clear: both;"></div>' +
                '</div>';
            return html;
        },
        /**点击事件*/
        itemClick: null
    };

    $this.baseCfg = {};

    /**左边显示的控件对象*/
    $this.leftCtrl = {
        domainName: '',
        custImg: '',
        custName: ''
    };

    initBaseCfg(defaultCfg, opts);

    /**
     * 加载数据
     * @param data
     */
    $this.resetData = function (contentHtml) {
        $this.baseCfg.contentHtml = contentHtml;
        $this.baseCfg.isReSetData = true;
        setSelectedImg();
    };

    /**构建控件*/
    buildCtrl();

    setSelectedImg();

    /**
     * 初始化配置
     * @param cfg
     * @param opts
     */
    function initBaseCfg(cfg, opts) {
        $this.baseCfg =
            $.extend(cfg, typeof(opts) == 'undefined' ? cfg : opts);

        $this.baseCfg.contentHtml =
            (typeof(opts.contentHtml) == 'undefined' ? [] : opts.contentHtml);

    }

    /**
     * 创建页面控件
     * @param $obj
     */
    function buildCtrl() {
        var html =
            '<h2 class="domainName">暂无信息</h2>' +
                '<span>' +
                '    <img class="custImg"' +
                ' src="' + $this.baseCfg.defalutImgUrl + '">' +
                '</span>' +
                '<a class="custName">暂无信息</a> ' +
                '<a class="arrowRi"></a>';

        $this.$container.append(html);

        html =
            '<div class="imgList shadow" ' +
                'id="' + $this.baseCfg.imgListId + '">' +
                '   <div class="imgCtrl" ' +
                'id="' + $this.baseCfg.imgCtrlId + '"></div>' +
                '   <div style="clear: both;"></div>' +
                '</div>';

        $('body').append(html);

        Util.shadowBorder('#' + $this.baseCfg.imgListId, 2, 2, 5, 5, '#D9D9D9');

        $('#' + $this.baseCfg.imgListId).hide();

        $this.leftCtrl.domainName = $('h2.domainName', $this.$container);
        $this.leftCtrl.custImg = $('span img.custImg', $this.$container);
        $this.leftCtrl.custName = $('a.custName', $this.$container);

        addFlag($this.$container);

        //点击箭头，打开图片列表
        var $arrow = $('a.arrowRi', $this.$container).click(function (e) {
            //设置显示出来的窗口位置及鼠标移开后的隐藏
            var obj = Util.getMousePositionObj(e);
            showImgListPanel(obj, $(this));
        });

        $this.$container.click(function (e) {
            //设置显示出来的窗口位置及鼠标移开后的隐藏
            var obj = Util.getMousePositionObj(e);
            showImgListPanel(obj, $(this));
        });

        //模拟失去焦点(原生失去焦点事件，在WP8平板上有问题)隐藏控件的效果
        $('*').click(function (e) {

            var imgListId = $('#' + $this.baseCfg.imgListId);

            if (imgListId.is(':hidden')) {
                return;
            }

            if ($(e.target).attr("flipsnap_id") != $this.baseCfg.imgListId) {
                imgListId.hide('slow');
            }

        });

    }

    /**
     * 对象添加特殊标识
     * @param $obj
     */
    function addFlag($obj) {
        $obj.find('*').attr('flipsnap_id', $this.baseCfg.imgListId);
        $obj.attr('flipsnap_id', $this.baseCfg.imgListId);
    }

    /**
     * 显示图片列表控件
     */
    function showImgListPanel(obj, $clickObj) {

        if ($this.baseCfg.imgListCtrl == null || $this.baseCfg.isReSetData) {
            $this.baseCfg.isReSetData = false;
            var contentHtml = [];

            for (var i = 0; i < $this.baseCfg.contentHtml.length; i++) {
                var img = $this.baseCfg.contentHtml[i].customImg;

                if (Util.isBlank(img)) {
                    $this.baseCfg.contentHtml[i].customImg =
                        $this.baseCfg.defalutImgUrl;
                }

                var html =
                    $this.baseCfg.getHtmlFormat(
                        $this.baseCfg.contentHtml[i], i);

                contentHtml.push(html);
            }

            $this.baseCfg.imgListCtrl =
                new BasePanel("#" + $this.baseCfg.imgCtrlId, {
                    /**面板可视范围内显示的元素个数，如果展开后，
                     * 则是disItem = disItem * expanRow*/
                    disItem: 4,
                    /**显示面板宽度*/
                    width: $this.baseCfg.showWidth,
                    /**面板里需要承载的html内容*/
                    contentHtml: contentHtml,
                    /**是否显示展开按钮*/
                    isExpan: false,
                    /**是否自动展开*/
                    isAutoExpan: true,
                    /**展开后显示的行数*/
                    expanRows: 4,
                    /**箭头位置：top：顶部；middle：中间*/
                    arrowAlign: 'none',
                    itemMarginTop: 0,
                    /**面板移动完成后事件*/
                    onmoveend: function (pageNo) {

                    },
                    itemClick: function (idx, clickHtml) {

                        var item = $this.baseCfg.contentHtml[idx];
                        setSelectedItem(item);

                        if ($this.baseCfg.itemClick) {
                            $this.baseCfg.itemClick.call(this, item, clickHtml);
                        }

                    }
                });

            $('div.itemSmall', $this.baseCfg.imgListCtrl.$container)
                .addClass('bottomLine')
                .parent()
                .find('div.bisItem:odd,span.container:odd,a.sName:odd')
                .addClass('logobg');

            addFlag($('#' + $this.baseCfg.imgCtrlId));
            addFlag($this.baseCfg.imgListCtrl.$container);
        }

        $("#" + $this.baseCfg.imgListId)
            .css('width', $this.baseCfg.showWidth + 1).animate({
                left: obj.x + 10,
                top: obj.y
            }, '300').fadeIn();
    }


    /**
     * 根据选中状态，设置域、图片、客户等
     */
    function setSelectedItem(item) {
        if (item == null) {
            return;
        }

        if (Util.isBlank(item.customImg)) {
            item.customImg = $this.baseCfg.defalutImgUrl;
        }

        $this.leftCtrl.domainName.text(item.domainName);
        $this.leftCtrl.custImg.attr('src', item.customImg);
        $this.leftCtrl.custName.text(item.customName);
    }

    /**
     * 找到选择的item
     */
    function findSelectedImg(contentHtml) {

        var item = null;

        for (var i = 0; i < contentHtml.length; i++) {
            var temp = contentHtml[i];
            if (temp.selected) {
                item = temp;
                break;
            }
        }

        return item;
    }

    /**
     *
     */
    function setSelectedImg() {
        var item = findSelectedImg($this.baseCfg.contentHtml);

        if (item == null) {
            return;
        }

        setSelectedItem(item);

    }
}