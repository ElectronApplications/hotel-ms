<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import { Bars3Icon, XMarkIcon } from "@heroicons/vue/24/outline";
import { Dialog, DialogPanel } from "@headlessui/vue";
import BrandIcon from "@/assets/brand-icon.svg";
import { computed, ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
import PrimaryButton from "@/components/PrimaryButton.vue";
import { useI18n } from "vue-i18n";
import { useLocale, type LocaleType } from "@/stores/locale";
import SelectListDynamic from "./components/SelectListDynamic.vue";

const BRAND_HOTEL_NAME = import.meta.env.VITE_BRAND_HOTEL_NAME;

const { t } = useI18n({
  messages: {
    en: {
      browserLanguage: "Browser language",
      reception: "Reception",
      service: "Service",
      cleaning: "Cleaning",
      planning: "Planning",
      admin: "Admin",
      book: "Book",
      profile: "Profile",
      login: "Login",
      closeMenu: "Close menu",
    },
    ru: {
      browserLanguage: "Язык браузера",
      reception: "Ресепшен",
      service: "Услуги",
      cleaning: "Уборка",
      planning: "Планировка",
      admin: "Админ",
      book: "Бронирование",
      profile: "Профиль",
      login: "Вход",
      closeMenu: "Закрыть меню",
    },
  },
});

const locale = useLocale();
const { currentLocale } = storeToRefs(locale);

const localesText = computed(() => [t("browserLanguage"), "English", "Русский"]);
const localesMap: (LocaleType | undefined)[] = [undefined, "en", "ru"];

const authStore = useAuthStore();
const { currentUser } = storeToRefs(authStore);

const mobileMenuOpen = ref(false);

const topEntries = computed(() => {
  return [
    {
      name: t("reception"),
      path: "/management/reception",
      enabled: currentUser.value?.role === "reception" || currentUser.value?.role === "admin",
    },
    {
      name: t("service"),
      path: "/management/service",
      enabled: currentUser.value?.role === "service" || currentUser.value?.role === "admin",
    },
    {
      name: t("cleaning"),
      path: "/management/cleaning",
      enabled: currentUser.value?.role === "cleaning" || currentUser.value?.role === "admin",
    },
    {
      name: t("planning"),
      path: "/management/planning",
      enabled: currentUser.value?.role === "planning" || currentUser.value?.role === "admin",
    },
    {
      name: t("admin"),
      path: "/management/admin",
      enabled: currentUser.value?.role === "admin",
    },
    {
      name: t("book"),
      path: "/book",
      enabled: currentUser.value !== undefined,
    },
    {
      name: t("profile"),
      path: "/profile",
      enabled: currentUser.value != undefined,
    },
  ].filter((entry) => entry.enabled);
});
</script>

<template>
  <header>
    <nav class="container mx-auto flex flex-row items-center justify-between p-4 text-sm">
      <div class="flex flex-row space-x-4">
        <RouterLink to="/" class="flex flex-row items-center">
          <BrandIcon class="size-[32px] pe-2" />
          <span class="font-extrabold">{{ BRAND_HOTEL_NAME }}</span>
        </RouterLink>

        <SelectListDynamic
          :options="localesText"
          :selected="localesMap.indexOf(currentLocale)"
          @updateSelection="(value) => locale.setLocale(localesMap[value])"
        />
      </div>

      <button class="block lg:hidden" @click="mobileMenuOpen = true">
        <span class="sr-only">Open menu</span>
        <Bars3Icon class="h-6 w-6" aria-hidden="true" />
      </button>

      <div class="hidden flex-row gap-x-10 lg:flex">
        <RouterLink
          v-for="entry in topEntries"
          v-bind:key="entry.path"
          :to="entry.path"
          class="font-bold"
          >{{ entry.name }}</RouterLink
        >
        <RouterLink v-if="currentUser === undefined" to="/login">
          <PrimaryButton class="px-8 py-3">{{ t("login") }}</PrimaryButton>
        </RouterLink>
      </div>

      <Dialog class="lg:hidden" @close="mobileMenuOpen = false" :open="mobileMenuOpen">
        <div class="fixed inset-0 z-10" />
        <DialogPanel
          class="fixed inset-y-0 right-0 z-10 w-full overflow-y-auto bg-surface-light px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10 dark:bg-surface-dark"
        >
          <div
            class="flex items-center justify-between text-surface-light dark:text-surface-content-dark"
          >
            <RouterLink
              to="/"
              @click="mobileMenuOpen = false"
              class="-m-1.5 flex flex-row items-center p-1.5"
            >
              <BrandIcon class="size-[32px] pe-2" />
              <span class="text-sm font-bold">{{ BRAND_HOTEL_NAME }}</span>
            </RouterLink>
            <button
              type="button"
              class="-m-2.5 rounded-md p-2.5 text-gray-700"
              @click="mobileMenuOpen = false"
            >
              <span class="sr-only">{{ t("closeMenu") }}</span>
              <XMarkIcon class="h-6 w-6 dark:text-white" aria-hidden="true" />
            </button>
          </div>

          <div class="flex flex-col gap-y-2 pt-5 text-lg font-semibold">
            <RouterLink
              v-for="entry in topEntries"
              v-bind:key="entry.path"
              :to="entry.path"
              @click="mobileMenuOpen = false"
              >{{ entry.name }}</RouterLink
            >
            <RouterLink v-if="currentUser === undefined" to="/login" @click="mobileMenuOpen = false"
              >{{ t("login") }}
            </RouterLink>
          </div>
        </DialogPanel>
      </Dialog>
    </nav>
  </header>

  <RouterView />
</template>
