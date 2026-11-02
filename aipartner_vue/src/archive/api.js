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

export function unlockExtra(id, answer) {
  return request('/unlock/extra', {
    method: 'POST',
    body: JSON.stringify({ id, answer }),
  })
}
