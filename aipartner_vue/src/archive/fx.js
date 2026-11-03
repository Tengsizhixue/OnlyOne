// 环境柔光：桌面跟随指针，手机跟随阅读位置缓慢下移。
// 只写 transform，不碰布局与重绘；柔光层在 .bg 里，永远不挡点击。

const REDUCED =
  typeof window !== 'undefined' &&
  window.matchMedia &&
  window.matchMedia('(prefers-reduced-motion: reduce)').matches

export function initAmbientLight() {
  if (typeof window === 'undefined' || REDUCED) return

  const bg = document.querySelector('.bg')
  if (!bg) return
  const lamp = bg.querySelector('.lamp')
  if (!lamp) return

  const fine =
    window.matchMedia &&
    window.matchMedia('(hover: hover) and (pointer: fine)').matches

  const show = () => {
    // 先落到目标位置再淡入，避免从角落滑进来那一下
    requestAnimationFrame(() => bg.classList.add('is-lamp'))
  }

  if (fine) {
    let raf = 0
    let x = window.innerWidth * 0.5
    let y = window.innerHeight * 0.32
    const place = () => {
      raf = 0
      lamp.style.transform = 'translate3d(' + x + 'px,' + y + 'px,0)'
    }
    place()
    show()
    window.addEventListener(
      'mousemove',
      (e) => {
        x = e.clientX
        y = e.clientY
        if (!raf) raf = requestAnimationFrame(place)
      },
      { passive: true }
    )
    return
  }

  // 触屏没有指针：让光按阅读进度在页面上缓缓下移，像手电扫过纸面
  let raf = 0
  let lastY = -999
  const place = () => {
    raf = 0
    const doc = document.documentElement
    const max = Math.max(1, doc.scrollHeight - window.innerHeight)
    const p = Math.min(1, Math.max(0, window.scrollY / max))
    const y = window.innerHeight * (0.26 + p * 0.46)
    if (Math.abs(y - lastY) < 4) return
    lastY = y
    lamp.style.transform = 'translate3d(' + window.innerWidth * 0.5 + 'px,' + y + 'px,0)'
  }
  place()
  show()

  const schedule = () => {
    if (!raf) raf = requestAnimationFrame(place)
  }
  window.addEventListener('scroll', schedule, { passive: true })
  window.addEventListener('resize', schedule, { passive: true })
}
