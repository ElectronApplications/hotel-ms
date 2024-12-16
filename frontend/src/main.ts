import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "@/App.vue";
import router from "@/router";

import "@/style.css";
import axios from "axios";
import { useAuthStore } from "@/stores/auth";
import { createI18n } from "vue-i18n";

axios.interceptors.request.use(async (config) => {
  const authStore = useAuthStore();

  if (await authStore.updateTokens()) {
    config.headers.Authorization = `Bearer ${authStore.access}`;
  }

  return config;
});

const app = createApp(App);

app.use(
  createI18n({
    legacy: false,
    fallbackLocale: "en",
    pluralRules: {
      ru: (choice: number, choicesLength: number) => {
        // Шаблон: 0 машин | {n} машина | {n} машины | {n} машин
        if (choice === 0) {
          return 0;
        }

        const teen = choice > 10 && choice < 20;
        const endsWithOne = choice % 10 === 1;

        if (choicesLength < 4) {
          return !teen && endsWithOne ? 1 : 2;
        }
        if (!teen && endsWithOne) {
          return 1;
        }
        if (!teen && choice % 10 >= 2 && choice % 10 <= 4) {
          return 2;
        }

        return choicesLength < 4 ? 2 : 3;
      },
    },
  }),
);

app.use(createPinia());
app.use(router);

app.mount("#app");
