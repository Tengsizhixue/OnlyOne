/**
 * 留言列表与留言提醒共用同一个节拍。
 *
 * 两处各自 setInterval 会从各自的挂载时刻起算，天然错开半拍；
 * 一旦提醒先到、列表后到，就会出现「提醒弹出来了，点进去却没有那条留言」。
 * 这里统一成同一个间隔，并把首次触发对齐到整刻度（Date.now() % 间隔），
 * 两个组件无论谁先挂载，都在同一秒发请求，看到的是同一份数据。
 */
export const POLL_MS = 30000

/** 距下一个整刻度的毫秒数 */
function nextTickDelay(ms) {
  return ms - (Date.now() % ms)
}

/**
 * 对齐节拍轮询：先等一个剩余片段，再按固定间隔跑。
 * 返回停止函数。
 */
export function startAlignedPoll(fn, ms = POLL_MS) {
  let interval = 0
  const first = window.setTimeout(() => {
    fn()
    interval = window.setInterval(fn, ms)
  }, nextTickDelay(ms))
  return () => {
    window.clearTimeout(first)
    if (interval) window.clearInterval(interval)
  }
}
