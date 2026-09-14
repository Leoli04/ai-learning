import DefaultTheme from 'vitepress/theme'
import './custom.css'
import AiSites from './AiSites.vue'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('AiSites', AiSites)
  }
}
