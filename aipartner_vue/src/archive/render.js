const ESCAPES = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }

function escapeHtml(value) {
  return String(value).replace(/[&<>"]/g, (ch) => ESCAPES[ch])
}

/**
 * 把描述里的 {{p001}} 换成真名；未解锁的阶段保持 ***。
 * 描述本身是可信的富文本，只有名字来自接口，做一次转义。
 */
export function renderTokens(html, names) {
  if (!html) return ''
  return html.replace(/\{\{(p\d{3})\}\}/g, (match, id) => {
    const name = names && names[id]
    return name ? escapeHtml(name) : '***'
  })
}
