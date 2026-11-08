const BASE = '/api/archive'

async function request(path, options = {}) {
  const res = await fetch(BASE + path, {
    credentials: 'same-origin',
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })

  let data = null
  try {
    data = await res.json()
  } catch (e) {
    // 非 JSON 响应，交给下面的状态码处理
  }

  if (!res.ok) {
    const message = data && data.detail ? data.detail : `请求失败（${res.status}）`
    throw new Error(message)
  }
  return data
}

export function getContent() {
  return request('/content')
}

export function getState() {
  return request('/state')
}

// 输对姓名/拼音/外号只揭示这一个人，不再整栏放开
export function unlockPerson(stage, name) {
  return request('/unlock/person', {
    method: 'POST',
    body: JSON.stringify({ stage, name }),
  })
}

// 附加内容的三道题：都填了就放行（后端不比对答案）
export function unlockExtra(stage, answers) {
  return request('/unlock/extra', {
    method: 'POST',
    body: JSON.stringify({ stage, answers }),
  })
}

// 答对才把图片地址发回来，答错后端不返回任何地址
export function unlockPhoto(album, answer) {
  return request('/unlock/photo', {
    method: 'POST',
    body: JSON.stringify({ album, answer }),
  })
}

export function listComments(person) {
  return request(`/comments?person=${encodeURIComponent(person)}`)
}

export function addComment(person, nick, body, parent = null) {
  const payload = { person, nick, body }
  if (parent) payload.parent = parent
  return request('/comments', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function deleteComment(id) {
  return request(`/comments/${id}`, { method: 'DELETE' })
}

// 留言提醒：只回「哪个人下面有新消息」，正文不在这里，所以不会漏内容
export function getNotifications(since) {
  return request(`/notifications?since=${Number(since) || 0}`)
}

// 作者模式：留言框里输暗号换一个服务端签名的 cookie，
// 之后发的留言由后端标成作者；身份判断完全在服务端，前端不传 role。
export function authorStatus() {
  return request('/author/status')
}

export function authorLogin(key) {
  return request('/author/login', {
    method: 'POST',
    body: JSON.stringify({ key }),
  })
}

export function authorLogout() {
  return request('/author/logout', { method: 'POST' })
}

export function pinComment(id, pinned) {
  return request(`/comments/${id}/pin`, {
    method: 'POST',
    body: JSON.stringify({ pinned }),
  })
}
