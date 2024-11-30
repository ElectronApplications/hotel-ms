<script setup lang="ts">
import { toRefs, type InputTypeHTMLAttribute } from "vue";

const props = withDefaults(
  defineProps<{
    enabled?: boolean;
    type?: InputTypeHTMLAttribute;
    name?: string;
    autocomplete?: string;
    required?: boolean;
    readonly?: boolean;
    placeholder?: string;
  }>(),
  {
    enabled: true,
    type: "text",
  },
);

const { enabled, type, name, autocomplete, required, readonly, placeholder } =
  toRefs(props);

const model = defineModel<string>();
</script>

<template>
  <input
    v-model="model"
    :name="name"
    :type="type"
    :autocomplete="autocomplete"
    :required="required"
    :readonly="readonly"
    :placeholder="placeholder"
    :disabled="!enabled"
    class="block w-full rounded-md border-0 bg-surface-light p-2 py-2 shadow-sm ring-1 ring-secondary-light sm:text-sm/6 dark:bg-surface-dark dark:ring-secondary-active-dark"
  />
</template>
