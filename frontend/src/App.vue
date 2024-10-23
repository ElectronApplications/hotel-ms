<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import { Bars3Icon, XMarkIcon } from "@heroicons/vue/24/outline";
import { Dialog, DialogPanel } from "@headlessui/vue";
import BrandIcon from "./assets/brand-icon.svg";
import { ref } from "vue";

const BRAND_HOTEL_NAME = import.meta.env.VITE_BRAND_HOTEL_NAME;

const mobileMenuOpen = ref(false);
</script>

<template>
  <header>
    <nav
      class="container sticky mx-auto flex flex-row items-center justify-between border-b border-gray-200 p-4 dark:border-slate-800"
    >
      <RouterLink to="/" class="flex flex-row items-center">
        <BrandIcon class="size-[32px] pe-2" />
        <span class="text-sm font-bold">{{ BRAND_HOTEL_NAME }}</span>
      </RouterLink>

      <button class="block lg:hidden" @click="mobileMenuOpen = true">
        <span class="sr-only">Open menu</span>
        <Bars3Icon class="h-6 w-6" aria-hidden="true" />
      </button>

      <div
        class="hidden flex-row gap-x-8 text-sm font-semibold text-gray-900 lg:flex dark:text-slate-300"
      >
        <a href="/admin">Django admin page</a>
        <RouterLink to="/vue-admin">Admin page</RouterLink>
      </div>

      <Dialog
        class="lg:hidden"
        @close="mobileMenuOpen = false"
        :open="mobileMenuOpen"
      >
        <div class="fixed inset-0 z-10" />
        <DialogPanel
          class="fixed inset-y-0 right-0 z-10 w-full overflow-y-auto bg-white px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10 dark:bg-slate-950"
        >
          <div class="flex items-center justify-between">
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

          <div
            class="flex flex-col gap-y-2 pt-5 text-lg font-semibold text-gray-900 dark:text-slate-300"
          >
            <a href="/admin">Django admin page</a>
            <RouterLink to="/vue-admin">Admin page</RouterLink>
          </div>
        </DialogPanel>
      </Dialog>
    </nav>
  </header>

  <RouterView />
</template>
