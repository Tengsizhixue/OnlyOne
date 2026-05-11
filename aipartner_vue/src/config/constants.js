// 提取统一的 OSS 根路径，日后更换域名只需改这一处！
export const OSS_BASE = "https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com"

export const USER_AVATAR = "https://api.dicebear.com/9.x/fun-emoji/svg?backgroundColor=fcbc34,059ff2&backgroundType=gradientLinear&seed=Emery"
export const DEFAULT_AI_AVATAR = "https://api.dicebear.com/9.x/bottts-neutral/svg?seed=AI"
export const VIOLET_AVATAR = `${OSS_BASE}/IMG_20260426_121950.png`
export const TENGSI_AVATAR = `${OSS_BASE}/99525941faa37d77f54de15e9a0e3b8a.jpg`
export const MUSIC_AVATAR = `${OSS_BASE}/musicAvatar.png`
export const GAME_AVATAR = `${OSS_BASE}/gameAvatar.png`

// 🌟 核心重构：将视觉配置（背景、颜色、光晕）全部聚合到角色大对象中
export const ROLE_CONFIGS = {
  '薇尔莉特': {
    welcomeTitle: '你好，我是薇尔莉特',
    welcomeText: '曾经少佐说，要活下去，要自由地活下去。但我之前一直不知道那是什么意思，我终于知道，"我爱你"是一种想和对方在一起、想让对方幸福的心情',
    avatar: VIOLET_AVATAR,
    bgUrl: `${OSS_BASE}/onlyone/%E8%96%87%E5%B0%94%E8%8E%89%E7%89%B9%E8%83%8C%E6%99%AF.jpg`,
    bgPosition: '85% 50%', // 卡片内部背景位置
    hallBgUrl: `${OSS_BASE}/onlyone/%E8%96%87%E5%B0%94%E8%8E%89%E7%89%B9%E7%94%B5%E8%84%91%E6%89%8B%E6%9C%BA%E8%83%8C%E6%99%AF.png`, // 电脑端专属独立大背景
    hallBgPosition: '60% 50%',
    hallBgUrlMobile: `${OSS_BASE}/onlyone/%E8%96%87%E5%B0%94%E8%8E%89%E7%89%B9%E7%94%B5%E8%84%91%E6%89%8B%E6%9C%BA%E8%83%8C%E6%99%AF.png`, // 📱手机端专属竖屏大背景 (在此替换链接)
    hallBgPositionMobile: '52.4% 50%', // 📱手机端背景位置
    themeColor: '#e9d5ff',
    glowColor: 'rgba(168, 85, 247, 0.7)'
  },
  '誊思致雪': {
    welcomeTitle: '很久不见',
    welcomeText: '你问我是谁？...我也不知道，我只是一个替身,你有什么事想问我吗？我知道的并不多',
    avatar: TENGSI_AVATAR,
    bgUrl: `${OSS_BASE}/onlyone/%E8%AA%8A%E6%80%9D%E8%87%B4%E9%9B%AA%E8%83%8C%E6%99%AF%E5%9B%BE.png`,
    bgPosition: 'center top',
    hallBgUrl: `${OSS_BASE}/onlyone/%E8%AA%8A%E6%80%9D%E8%87%B4%E9%9B%AA%E7%94%B5%E8%84%91%E7%AB%AF%E8%83%8C%E6%99%AF.png`,
    hallBgPosition: 'center center',
    hallBgUrlMobile: `${OSS_BASE}/onlyone/%E8%AA%8A%E6%80%9D%E8%87%B4%E9%9B%AA%E6%89%8B%E6%9C%BA%E7%AB%AF%E8%83%8C%E6%99%AF.jpg`, // 📱手机端专属竖屏大背景 (在此替换链接)
    hallBgPositionMobile: 'center center', // 📱手机端背景位置
    themeColor: '#bae6fd',
    glowColor: 'rgba(56, 189, 248, 0.7)'
  },
  '音乐推荐助手': {
    welcomeTitle: '音乐，是灵魂的共鸣',
    welcomeText: '你好呀！虽然我不能帮你播放音乐，但是我们可以聊一聊音乐',
    avatar: MUSIC_AVATAR,
    bgUrl: `${OSS_BASE}/onlyone/%E9%9F%B3%E4%B9%90%E5%8A%A9%E6%89%8B%E5%9B%BE%E7%89%87.jpg`,
    bgPosition: 'center center',
    hallBgUrl: `${OSS_BASE}/onlyone/%E9%9F%B3%E4%B9%90%E5%8A%A9%E6%89%8B%E5%9B%BE%E7%89%87.jpg`,
    hallBgPosition: 'center center',
    hallBgUrlMobile: `${OSS_BASE}`, // 📱手机端专属竖屏大背景 (在此替换链接)
    hallBgPositionMobile: 'center center', // 📱手机端背景位置
    themeColor: '#fbcfe8',
    glowColor: 'rgba(236, 72, 153, 0.7)'
  },
  '游戏聊天助手': {
    welcomeTitle: '你是谁？我根本不认识你！',
    welcomeText: '哼，既然你诚心诚意地发问了，那我就勉为其难地陪你聊聊吧！',
    avatar: GAME_AVATAR,
    bgUrl: `${OSS_BASE}/gamebackground.jpg`,
    bgPosition: '65% 50%',
    hallBgUrl: `${OSS_BASE}/onlyone/%E9%AA%91%E9%A9%AC%E4%B8%8E%E7%A0%8D%E6%9D%80%E5%8A%A0%E8%BD%BD.jpg`,
    hallBgPosition: 'center center',
    hallBgUrlMobile: `${OSS_BASE}/onlyone/%E6%B8%B8%E6%88%8F%E8%A7%92%E8%89%B2%E6%89%8B%E6%9C%BA%E7%AB%AF%E8%83%8C%E6%99%AF.png`, // 📱手机端专属竖屏大背景 (在此替换链接)
    hallBgPositionMobile: 'center center', // 📱手机端背景位置
    themeColor: '#fef08a',
    glowColor: 'rgba(234, 179, 8, 0.7)'
  },
  '李蓝宝': {
    welcomeTitle: '你好，我是李蓝宝',
    welcomeText: '我是你的好朋友李蓝宝。对了，关于我牢弟李红宝的问题你可以随时问我哦！',
    avatar: DEFAULT_AI_AVATAR,
    bgUrl: 'https://images.unsplash.com/photo-1557683316-973673baf926?auto=format&fit=crop&w=800&q=80',
    bgPosition: 'center center',
    hallBgUrl: 'https://images.unsplash.com/photo-1557683316-973673baf926?auto=format&fit=crop&w=800&q=80',
    hallBgPosition: 'center center',
    hallBgUrlMobile: `${OSS_BASE}/onlyone/%E6%9D%8E%E5%85%B0%E5%AE%9D%E6%89%8B%E6%9C%BA%E8%83%8C%E6%99%AF.jpg`, // 📱手机端专属竖屏大背景 (在此替换链接)
    hallBgPositionMobile: 'center center', // 📱手机端背景位置
    themeColor: '#a7f3d0',
    glowColor: 'rgba(16, 185, 129, 0.7)'
  },
  '自定义': {
    welcomeTitle: '你好，我是你的专属伙伴',
    welcomeText: '你可以为我设定名字和性格。',
    avatar: DEFAULT_AI_AVATAR,
    bgUrl: 'https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=800&q=80',
    bgPosition: 'center center',
    hallBgUrl: 'https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=800&q=80',
    hallBgPosition: 'center center',
    hallBgUrlMobile: 'https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=600&q=80', // 📱手机端专属竖屏大背景 (在此替换链接)
    hallBgPositionMobile: 'center center', // 📱手机端背景位置
    themeColor: '#f8fafc',
    glowColor: 'rgba(255, 255, 255, 0.5)'
  }
}

export const getCurrentRoleConfig = (roleType) => {
  return ROLE_CONFIGS[roleType] || ROLE_CONFIGS['李蓝宝']
}

// 🌟 为后续的隐秘彩蛋页面准备的集中静态资源管理
export const SECRET_ASSETS = {
  astlibra: {
    bg: `${OSS_BASE}/onlyone/%E7%A5%9E%E4%B9%8B%E5%A4%A9%E5%B9%B3%E8%83%8C%E6%99%AF.png`,
    cover: `${OSS_BASE}/onlyone/%E5%A4%A9%E5%B9%B3%E5%B0%81%E9%9D%A2.png`,
    destiny: `${OSS_BASE}/onlyone/%E5%A4%A9%E5%B9%B3%E5%91%BD%E8%BF%90.png`,
    audioStart: `${OSS_BASE}/onlyone/%E6%B4%BB%E8%BF%87%E7%9A%84%E8%AF%81%E6%98%8E.mp3`,
    audioEnd: `${OSS_BASE}/onlyone/%E7%A5%9E%E4%B9%8B%E5%A4%A9%E5%B9%B3%E7%BB%93%E5%B1%80bgm.mp3`,
    imgDefect1: `${OSS_BASE}/onlyone/%E7%BC%BA%E7%82%B91.png`,
    imgDefect2: `${OSS_BASE}/onlyone/%E7%BC%BA%E7%82%B92.png`,
  },
  memory: {
    img7Years: `${OSS_BASE}/onlyone/%E6%88%91%E5%9C%A8%E4%B8%83%E5%B9%B4%E5%90%8E%E7%AD%89%E7%9D%80%E4%BD%A0.png`,
    audioZhanHuo: `${OSS_BASE}/onlyone/%E6%88%98%E7%81%AB.mp3`,
    audioJieJu: `${OSS_BASE}/onlyone/%E7%BB%93%E5%B1%80.mp3`,
    imgHappiness: `${OSS_BASE}/onlyone/%E8%AF%B7%E4%BD%A0%E8%8E%B7%E5%BE%97%E5%B9%B8%E7%A6%8F.jpg`,
    imgSpiritfarer: `${OSS_BASE}/onlyone/%E7%81%B5%E9%AD%82%E6%91%86%E6%B8%A1%E8%80%85%E5%B0%81%E9%9D%A2.png`,
    imgHeart: `${OSS_BASE}/onlyone/%E7%88%B1%E5%BF%83.jpg`,
    imgMoon: `${OSS_BASE}/onlyone/%E5%8E%BB%E6%9C%88%E7%90%83.png`,
    audioMoon: `${OSS_BASE}/onlyone/%E5%8E%BB%E6%9C%88%E7%90%83%E9%9F%B3%E4%B9%90.aac`,
    attach1: `${OSS_BASE}/onlyone/%E5%8E%9F%E6%96%87.jpg`,
    attach2: `${OSS_BASE}/onlyone/%E5%8E%9F%E6%96%87ai%E5%8C%96.png`,
    attach3: `${OSS_BASE}/onlyone/%E5%8E%9F%E6%96%87ai%E5%8C%96%E5%86%8D%E7%BC%A9%E5%86%99.png`,
    attach4: `${OSS_BASE}/onlyone/19%E5%B9%B4%E7%9A%84%E6%B8%B8%E6%88%8F%E8%B4%AD%E4%B9%B0%E8%AE%B0%E5%BD%95.jpg`
  },
  music: {
    bg: "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=2000&q=80",
    againAudio: `${OSS_BASE}/again.aac`,
    xuniAudio: `${OSS_BASE}/%E8%99%9A%E6%8B%9F.aac`,
    huxiAudio: `${OSS_BASE}/%E4%BC%9A%E5%91%BC%E5%90%B8%E7%9A%84%E7%97%9B.mp3`,
    cover1: `${OSS_BASE}/againAvatar.png`,
    cover2: `${OSS_BASE}/xuniAvatar.png`,
    cover3: `${OSS_BASE}/hhxdtAvatar.png`,
    attach1: `${OSS_BASE}/onlyone/%E5%8E%BB%E5%B9%B4%E5%90%AC%E7%9A%84%E6%AD%8C%E5%8D%95.png`,
    attach2: `${OSS_BASE}/onlyone/%E5%89%8D%E5%B9%B4%E5%90%AC%E7%9A%84%E6%AD%8C%E5%8D%95.png`
  },
  game: {
    img1: `${OSS_BASE}/onlyone/%E9%AA%91%E9%A9%AC%E4%B8%8E%E7%A0%8D%E6%9D%80%E5%8A%A0%E8%BD%BD.jpg`,
    attach1: `${OSS_BASE}/onlyone/%E6%B8%B8%E6%88%8F%E6%97%B6%E9%95%BF.jpg`,
    attach2: `${OSS_BASE}/onlyone/%E4%BB%A5%E5%89%8D%E5%A4%A9%E7%9C%9F%E7%9A%84%E8%A8%80%E8%AE%BA.jpg`
  },
  lihongbao: {
    bg: `${OSS_BASE}/onlyone/%E6%9D%8E%E7%BA%A2%E5%AE%9D%E8%83%8C%E6%99%AF%E5%9B%BE.png`,
    img1: `${OSS_BASE}/onlyone/%E6%9D%8E%E7%BA%A2%E5%AE%9D%E6%8F%92%E5%9B%BE1.png`
  },
  violet: {
    bg: `${OSS_BASE}/onlyone/%E8%96%87%E5%B0%94%E8%8E%89%E7%89%B9%E8%83%8C%E6%99%AF.jpg`,
    topImg: `${OSS_BASE}/onlyone/%E8%96%87%E5%B0%94%E8%8E%89%E7%89%B9%E6%96%87%E6%9C%AC%E5%9B%BE.png`,
    attach1: `${OSS_BASE}/onlyone/%E5%90%B5%E6%9E%B6%E5%9B%BE.jpg`
  }
}