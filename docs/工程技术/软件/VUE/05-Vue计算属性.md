# 计算属性

## setter 和 getter

```html
<div id="app">
  <h2>{{fullName}}</h2>
  <h2>{{fullName1}}</h2>
  <h2>{{getFullName()}}</h2>
</div>
<script src="../js/vue.js"></script>
<script>
  const app = new Vue({
    el: '#app', // 用于挂在要管理的元素
    data: { // 定义数据
      firstName: '林青霞',
      lastName: '刘亦菲'
    },
    computed: {
      fullName: {
        set: function () {// 可以省略表示只读
        },
        get: function () {
          return this.firstName + '1' + this.lastName
        }
      },
      fullName1: function () {
        return this.firstName + '2' + this.lastName
      }
    },
    methods: {
      getFullName: function () {
        return this.firstName + '3' + this.lastName
      }
    }
  })
</script>
```

- 计算属性的缓存 , 如果多次调用 , 计算属性只会使用一次
