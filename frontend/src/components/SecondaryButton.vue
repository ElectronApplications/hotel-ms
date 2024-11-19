<script setup lang="ts">
import type { ButtonHTMLAttributes } from "vue";

const { enabled = true, type = "button" } = defineProps<{
  enabled?: boolean;
  type?: ButtonHTMLAttributes["type"];
}>();
</script>

<template>
  <button
    class="rounded-lg bg-secondary-light px-4 py-2 text-sm font-bold text-secondary-content-light duration-100 dark:bg-secondary-dark dark:text-secondary-content-dark"
    :class="[
      enabled
        ? 'hover:bg-secondary-active-light dark:hover:bg-secondary-active-dark'
        : '',
    ]"
    :type="type"
    :disabled="!enabled"
  >
    <slot>Button</slot>
  </button>
</template>
