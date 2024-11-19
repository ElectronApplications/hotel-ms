<script setup lang="ts">
const { enabled = true, type = "button" } = defineProps<{
  enabled?: boolean;
  type?: "button" | "submit" | "reset";
}>();
</script>

<template>
  <button
    class="rounded-lg bg-primary-light px-4 py-2 text-sm font-bold text-primary-content-light duration-100 dark:bg-primary-dark dark:text-primary-content-dark"
    :class="[
      enabled
        ? 'hover:bg-primary-active-light dark:hover:bg-primary-active-dark'
        : '',
    ]"
    :type="type"
    :disabled="!enabled"
  >
    <slot>Button</slot>
  </button>
</template>
