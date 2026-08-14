# 表单绑定 v-model

- 表单控件在实际开发是十分常见的 . 特别对于用户信息的提交 , 需要大量的表单
- Vue中使用`v-mode`指令来实现表单元素和数据的双向绑定

# v-model原理

- `v-model`其实是一个语法糖 , 它的背后包含两个操作
	- `v-bind` 绑定一个value属性
	- `v-on`指令给当前元素绑定input事件

# 修饰符

1. lazy修饰符
	- 默认情况下 , v-model 是与input事件中同步输入框的数据
	- lazy 则是在失去焦点 或 回车时才会更新
2. number修饰符
	- 可以将输入框的内容直接转换为数字类型
3. trim修饰符
	- 可以过滤输入内容左右两侧的空格

## input实例

```html
<div id="app">
  <input type="text" v-model="msg">
  <button @click="addData"></button>
</div>
<script src="../js/vue.js"></script>
<script>
  const app = new Vue({
    el: '#app',// 用于挂在要管理的元素
    data: {// 定义数据
      msg: "大家好,我是渣渣辉"
    },
    methods: {
      addData() {
        this.msg = "大家好,我是张家辉"
      }
    }
  })
</script>
```

## rodio实例

```html
<div id="app">
  <h4>{{msg}}</h4>
  <input type="radio" name="sex" v-model="msg" value="男"> 男
  <input type="radio" name="sex" v-model="msg" value="女"> 女
  <button @click="men">男</button>
  <button @click="women">女</button>
</div>
<script src="../js/vue.js"></script>
<script>
  const app = new Vue({
    el: '#app',// 用于挂在要管理的元素
    data: {// 定义数据
      msg: "男"
    },
    methods: {
      men() {
        this.msg = "男"
      }, women() {
        this.msg = "女"
      }
    }
  })
</script>
```

## checkbox实例

```html
<div id="app">
  <input type="checkbox" name="d" v-model="msg" value="篮球"> 篮球
  <input type="checkbox" name="d" v-model="msg" value="足球"> 足球
  <input type="checkbox" name="d" v-model="msg" value="乒乓球"> 乒乓球
  <input type="checkbox" name="d" v-model="msg" value="羽毛球"> 羽毛球
  <h4>{{msg}}</h4>
</div>
<script src="../js/vue.js"></script>
<script>
  const app = new Vue({
    el: '#app',// 用于挂在要管理的元素
    data: {// 定义数据
      msg: []
    },
    methods: {

    }
  })
</script>
```

## select实例

```html
<div id="app">
  <select name="m" id="" v-model="msg">
    <option value="游泳">游泳</option>
    <option value="跑步">跑步</option>
    <option value="自行车">自行车</option>
  </select>
  <h4>{{msg}}</h4>
</div>
<script src="../js/vue.js"></script>
<script>
  const app = new Vue({
    el: '#app',// 用于挂在要管理的元素
    data: {// 定义数据
      msg: []
    },
    methods: {

    }
  })
</script>
```

