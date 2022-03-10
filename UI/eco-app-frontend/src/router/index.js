import { createRouter, createWebHashHistory } from 'vue-router'
import GUIView from "../views/GUIView";

const routes = [
  {
    path: '/',
    component: GUIView
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
