# Vue实例传入的options

- el
  - 类型 : string | HTMLElement
  - 作用 : 决定之后Vue实例会管理哪一个dom
- data
  - 类型 : object | function (组件必须是函数)
  - 作用 : Vue实例对应的数据对象
- methods :
  - 类型 : `{ [key:string ] : function}`
  - 作用 : 定义属于Vue的一些方法 , 可以在其他地方调用 , 也可以在指令中调用
