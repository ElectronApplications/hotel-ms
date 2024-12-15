<script setup lang="ts">
import { nextTick, ref, toRefs, watch } from "vue";

const props = defineProps<{
  value: boolean;
}>();

const { value } = toRefs(props);

const emit = defineEmits<{
  updateValue: [value: boolean];
}>();

const model = ref(false);

watch(
  value,
  (v) => {
    nextTick(() => {
      model.value = v;
    });
  },
  {
    immediate: true,
  },
);

function updateValue() {
  emit("updateValue", model.value);
  nextTick(() => {
    model.value = value.value;
  });
}
</script>

<template>
  <input type="checkbox" v-model="model" @change="updateValue" />
</template>
