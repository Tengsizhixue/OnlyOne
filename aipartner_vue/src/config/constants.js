// 这个文件专门用来存放不会变动的常量和配置，以后加新角色都在这里加，不会弄脏视图代码
export const USER_AVATAR = "https://api.dicebear.com/9.x/fun-emoji/svg?backgroundColor=fcbc34,059ff2&backgroundType=gradientLinear&seed=Emery"
export const DEFAULT_AI_AVATAR = "https://api.dicebear.com/9.x/bottts-neutral/svg?seed=AI"
export const VIOLET_AVATAR = "https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com/IMG_20260426_121950.png"
export const TENGSI_AVATAR = "https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com/99525941faa37d77f54de15e9a0e3b8a.jpg"

// 新增角色的占位头像（你可以随时修改为你自己的图片链接）
export const MUSIC_AVATAR = "https://api.dicebear.com/9.x/bottts-neutral/svg?seed=MusicBot&backgroundColor=ffdfbf"
// [修改] 将游戏助手头像改为暗黑/青铜色调
export const GAME_AVATAR = "https://api.dicebear.com/9.x/bottts-neutral/svg?seed=KnightBot&backgroundColor=2A1D14"

export const ROLE_CONFIGS = {
  '薇尔莉特': {
    welcomeTitle: '你好，我是薇尔莉特',
    welcomeText: '曾经少佐说，要活下去，要自由地活下去。但我之前一直不知道那是什么意思，我终于知道，"我爱你"是一种想和对方在一起、想让对方幸福的心情',
    avatar: VIOLET_AVATAR
  },
  '誊思致雪': {
    welcomeTitle: '很久不见',
    welcomeText: '你问我是谁？...我也不知道，我只是一个替身,你有什么事想问我吗？我知道的并不多',
    avatar: TENGSI_AVATAR
  },
  '音乐推荐助手': {
    welcomeTitle: '音乐，是灵魂的共鸣',
    welcomeText: '你好呀！虽然我不能帮你播放音乐，但是我们可以聊一聊音乐',
    avatar: MUSIC_AVATAR
  },
  '游戏聊天助手': {
    welcomeTitle: '你是谁？我根本不认识你！',
    welcomeText: '哼，既然你诚心诚意地发问了，那我就勉为其难地陪你聊聊吧！',
    avatar: GAME_AVATAR
  },
  '自定义': {
    welcomeTitle: '你好，我是李蓝宝',
    welcomeText: '我是自定义角色，不代表任何人物，你可以随意修改我的性格与名称。我只有一个特殊设定：李红宝是我牢弟，关于他的问题你可以问我',
    avatar: DEFAULT_AI_AVATAR
  }
}

// 导出一个获取配置的方法
export const getCurrentRoleConfig = (roleType) => {
  return ROLE_CONFIGS[roleType] || ROLE_CONFIGS['自定义']
}