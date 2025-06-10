import { type Serve } from "bun";

const api = {
  auth: {
    async login(username: string, password: string) {
      return {
        // username,
        // password,
        token: 'jwt token...'
      }
    },
    async register(username: string, password: string){
      // 添加到数据库
      return;
    }
  },

  lesson: {
    // 函数1
  }
}


// 下面这一段不要改
type ApiType = typeof api

export default {
  async fetch(req) {
    try {
      const url = new URL(req.url)
      const [appName, moduleName, methodName] = url.pathname.slice(1).split('/');
      const module = api[moduleName as keyof ApiType]
      const body = await req.json() as []
      if (typeof module[methodName as keyof typeof module] !== 'function') {
        throw new Error(`Method ${methodName} is not a function`);
      }
      const method = module[methodName as keyof typeof module] as (...args: any[]) => Promise<any>;
      const result = await method(...body)
      return Response.json(result)
    } catch (err: any) {
      return new Response(err.message, { status: 500 })
    }
  }
} as Serve