```html
<div id="app">
  <h4>{{msg1}}</h4>
  <ul>
    <li v-for="item in list">{{item}}</li>
  </ul>
  <h4>{{msg1}}</h4>
  <ul>
    <li v-for="(item , index) in list">{{item}} - {{index}}</li>
  </ul>
  <h4>{{msg2}}</h4>
  <ul>
    <li v-for="item in ojb">{{item}}</li>
  </ul>
  <h4>{{msg3}}</h4>
  <ul>
    <li v-for="(val,key) in ojb">{{val}}.{{key}}</li>
  </ul>
  <h4>{{msg4}}</h4>
  <ul>
    <li v-for="(val,key,index) in ojb">{{val}}.{{key}}.{{index}}</li>
  </ul>
</div>
<script src="../js/vue.js"></script>
<script>
  const app = new Vue({
    el: '#app',// 用于挂在要管理的元素
    data: {// 定义数据
      msg1: "数组",
      msg1: "数组+index",
      msg2: "对象",
      msg3: "对象:key+value",
      msg4: "对象:key+value+index",
      list: [
        '海王', '星际穿越', '大话西游', '盗梦空间', '黑客帝国'
      ],
      ojb: {
        name: "luke",
        age: 28,
        home: "西安",
        sex: '男'
      }
    }
  })
</script>
```

