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

export function unlockStage(stage, name) {
  return request('/unlock/stage', {
    method: 'POST',
    body: JSON.stringify({ stage, name }),
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
