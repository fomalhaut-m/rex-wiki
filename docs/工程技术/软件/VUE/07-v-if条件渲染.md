# v-if

- `v-if` \ `v-else-if` \ `v-else`
- Vue条件指令可以根据表达式的值在DOM中渲染或销毁元素或组件
- v-if 后面的条件为false是 , 对应的元素不会渲染 , 也就是说根本不会有标签出现在DOM中

```html
<div id="app">
  <h2 v-if="flag">来呀</h2>
  <h3>{{score}}</h3>
  <h2 v-if="score>3">优</h2>
  <h2 v-else-if="score>2">良</h2>
  <h2 v-else >差</h2>
  <h3>{{flag}}</h3>
  <button @click="reversal()">v-if</button>
  <button @click="reversal()">翻转</button>
  <button @click="add()">add</button>
</div>
<script src="../js/vue.js"></script>
<script>
  const app = new Vue({
    el: '#app',
    data: {
      flag: true,
      score: 0
    },
    methods: {
      reversal() {
        this.flag = !this.flag;
      },
      add() {
        this.score++
      }
    }
  })
</script>
```
