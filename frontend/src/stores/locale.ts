import { useLocalStorage } from "@vueuse/core";
import { defineStore } from "pinia";
import { onBeforeMount } from "vue";
import { useI18n } from "vue-i18n";

export const locales = ["en", "ru"] as const;
export type LocaleType = (typeof locales)[number];

export const useLocale = defineStore("locale", () => {
  const currentLocale = useLocalStorage<LocaleType | undefined>("locale", undefined);

  const { locale } = useI18n();

  function updateLocale() {
    if (currentLocale.value !== undefined) {
      locale.value = currentLocale.value;
    } else {
      const browserLocale = window.navigator.language.substring(0, 2);
      console.log(browserLocale);
      locale.value = (locales as readonly string[]).includes(browserLocale) ? browserLocale : "en";
    }
  }

  function setLocale(newLocale?: LocaleType) {
    currentLocale.value = newLocale;
    updateLocale();
  }

  onBeforeMount(async () => {
    updateLocale();
  });

  return {
    currentLocale,
    setLocale,
  };
});
