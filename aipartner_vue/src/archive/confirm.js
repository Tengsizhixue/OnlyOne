// 全页共用一个确认框。
//
// 不用 window.confirm：微信内置浏览器（X5 / iOS WKWebView）会把它降级成
// 「是否关闭网页」的系统提示，或者直接吞掉不返回。
//
// 任何组件都能 `await askConfirm('要删吗？', '删掉')`，页面上只挂一个
// <ConfirmDialog />（见 ArchiveApp.vue）。对话框会 teleport 到 body，
// 这一点是必须的：留言区外面套着 content-visibility:auto 的栏，
// 它会让后代元素的 position:fixed 变成「相对这一栏」，于是弹窗跟着页面滚。
import { reactive } from 'vue'

export const confirmState = reactive({
  open: false,
  message: '',
  okText: '确定',
})

let resolver = null

export function askConfirm(message, okText = '确定') {
  // 上一条还挂着就先当作取消，避免 promise 悬空
  if (resolver) settleConfirm(false)
  confirmState.message = message
  confirmState.okText = okText
  confirmState.open = true
  return new Promise((resolve) => {
    resolver = resolve
  })
}

export function settleConfirm(ok) {
  const done = resolver
  resolver = null
  confirmState.open = false
  if (done) done(!!ok)
}
