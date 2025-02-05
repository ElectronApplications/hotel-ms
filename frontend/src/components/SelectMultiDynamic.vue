<script setup lang="ts">
import { nextTick, ref, toRefs, watch } from "vue";
import SelectMulti from "@/components/SelectMulti.vue";

const props = withDefaults(
  defineProps<{
    options: string[];
    selected: number[];
    placeholder?: string;
    maxTagsShow?: number;
  }>(),
  {
    placeholder: "Select options",
    maxTagsShow: 2,
  },
);

const { options, selected, placeholder, maxTagsShow } = toRefs(props);

const emit = defineEmits<{
  updateSelections: [options: number[]];
}>();

const selectedOptions = ref<number[]>([]);

watch(
  selected,
  (value) => {
    nextTick(() => {
      selectedOptions.value = value.slice();
    });
  },
  {
    immediate: true,
  },
);

function updateSelections() {
  emit("updateSelections", selectedOptions.value);
  nextTick(() => {
    selectedOptions.value = selected.value;
  });
}
</script>

<template>
  <SelectMulti @updateSelections="updateSelections" v-model="selectedOptions" :options="options"
    :placeholder="placeholder" :maxTagsShow="maxTagsShow" />
</template>
