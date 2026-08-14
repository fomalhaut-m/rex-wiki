# 事件监听

## 

## v-on

- 作用 : 绑定时间监听+
- 缩写 : `@`
- 预期 : `Function` | `Inline Statement` | `Object`
- 参数 : `event`

## 基本用法

```html
<div id="app">
  <h2>{{counter}}</h2>
  <button v-on:click="add">+</button><!-- 没有参数时可以不写小括号 -->
  <button @click="sub()">-</button>
</div>
<script src="../js/vue.js"></script>
<script>
  const app = new Vue({
    el: '#app',
    data: {
      counter: 0
    },
    methods: {
      add() {
        this.counter++;
      },
      sub(){
        this.counter--;
      }
    }
  })
</script>
```

## 参数传递

- 如果方法没有额外参数 , 后面可以不加()
	- 但是如果方法本身有参数 , 那么会默认将 event 事件作为参数传入
- 如果需要同时传入某个参数 , 同时需要 event , 可以通过`$event`传入事件

```html
<div id="app">
  <h2>{{counter}}</h2>
  <button v-on:click="add1">+1</button>
  <button @click="add2()">+2</button>
  <button @click="addStr1('你好')">有参</button>
  <button @click="addStr2">有参没传 $event</button>
  <button @click="addStr3($event,'我也好')">$event + 参数</button>
</div>
<script src="../js/vue.js"></script>
<script>
  const app = new Vue({
    el: '#app',
    data: {
      counter: '0 '
    },
    methods: {
      add1() {
        this.counter += '+ 1 ';
      },
      add2() {
        this.counter += '+ 4 ';
      },
      addStr1(str) {
        this.counter += '+ ' + str + ' ';
      },
      addStr2(event) {
        this.counter += '+ ' + event.type + ' ';
        console.log(event)
      },
      addStr3(event,str) {
        this.counter += '+ ' + str + ' ';
        console.log(event)
      },
    }
  })
</script>
```

