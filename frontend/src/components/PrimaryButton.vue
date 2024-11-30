<script setup lang="ts">
import { toRefs, type ButtonHTMLAttributes } from "vue";

const props = withDefaults(
  defineProps<{
    enabled?: boolean;
    type?: ButtonHTMLAttributes["type"];
  }>(),
  {
    enabled: true,
    type: "button",
  },
);

const { enabled, type } = toRefs(props);
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
