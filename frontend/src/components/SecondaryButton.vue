<script setup lang="ts">
import { toRefs, type ButtonHTMLAttributes } from "vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n({
  messages: {
    en: {
      button: "Button",
    },
    ru: {
      button: "Кнопка",
    },
  },
});

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
  <button class="rounded-lg px-4 py-2 text-sm font-bold duration-100" :class="[
    enabled
      ? 'bg-secondary-light text-secondary-content-light hover:bg-secondary-active-light dark:bg-secondary-dark dark:text-secondary-content-dark dark:hover:bg-secondary-active-dark'
      : 'bg-secondary-disabled-light text-secondary-disabled-content-light dark:bg-secondary-disabled-dark dark:text-secondary-disabled-content-dark',
  ]" :type="type" :disabled="!enabled">
    <slot>{{ t("button") }}</slot>
  </button>
</template>
