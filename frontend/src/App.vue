<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import { Bars3Icon, XMarkIcon } from "@heroicons/vue/24/outline";
import { Dialog, DialogPanel } from "@headlessui/vue";
import BrandIcon from "@/assets/brand-icon.svg";
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
import PrimaryButton from "@/components/PrimaryButton.vue";

const BRAND_HOTEL_NAME = import.meta.env.VITE_BRAND_HOTEL_NAME;

const authStore = useAuthStore();
const { currentUser } = storeToRefs(authStore);

const mobileMenuOpen = ref(false);
</script>

<template>
  <header>
    <nav
      class="container mx-auto flex flex-row items-center justify-between p-4 text-sm"
    >
      <RouterLink to="/" class="flex flex-row items-center">
        <BrandIcon class="size-[32px] pe-2" />
        <span class="font-bold">{{ BRAND_HOTEL_NAME }}</span>
      </RouterLink>

      <button class="block lg:hidden" @click="mobileMenuOpen = true">
        <span class="sr-only">Open menu</span>
        <Bars3Icon class="h-6 w-6" aria-hidden="true" />
      </button>

      <div class="hidden flex-row gap-x-8 lg:flex">
        <RouterLink v-if="currentUser === undefined" to="/login"
          ><PrimaryButton class="px-8 py-3">Login</PrimaryButton></RouterLink
        >
      </div>

      <Dialog
        class="lg:hidden"
        @close="mobileMenuOpen = false"
        :open="mobileMenuOpen"
      >
        <div class="fixed inset-0 z-10" />
        <DialogPanel
          class="fixed inset-y-0 right-0 z-10 w-full overflow-y-auto bg-surface-light px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10 dark:bg-surface-dark"
        >
          <div
            class="flex items-center justify-between text-surface-light dark:text-surface-content-dark"
          >
            <a href="#" class="-m-1.5 flex flex-row items-center p-1.5">
              <BrandIcon class="size-[32px] pe-2" />
              <span class="text-sm font-bold">{{ BRAND_HOTEL_NAME }}</span>
            </a>
            <button
              type="button"
              class="-m-2.5 rounded-md p-2.5 text-gray-700"
              @click="mobileMenuOpen = false"
            >
              <span class="sr-only">Close menu</span>
              <XMarkIcon class="h-6 w-6 dark:text-white" aria-hidden="true" />
            </button>
          </div>

          <div class="flex flex-col gap-y-2 pt-5 text-lg font-semibold">
            <RouterLink v-if="currentUser === undefined" to="/login"
              >Login</RouterLink
            >
          </div>
        </DialogPanel>
      </Dialog>
    </nav>
  </header>

  <RouterView />
</template>
