export type Status =
  'stopped' | 'connecting' | 'ready' | 'translating' |
  'listening' | 'recording' | 'synthesising' | 'outputting'

export interface ConsoleLog {
  type: 'info' | 'warn' | 'error'
  content: string
}

export interface Message {
  role: 'Stella' | 'You'
  content: string
  translation: string
  end: boolean
}
