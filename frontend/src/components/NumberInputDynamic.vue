<script setup lang="ts">
import { nextTick, ref, toRefs, watch } from "vue";
import NumberInput from "@/components/NumberInput.vue";

const props = defineProps<{
  numberValue: number;
  name?: string;
  placeholder?: string;
  required?: boolean;
}>();

const { numberValue, name, placeholder, required } = toRefs(props);

const emit = defineEmits<{
  updateValue: [value: number];
}>();

const inputValue = ref<number>(numberValue.value);
watch(numberValue, (value) => {
  inputValue.value = value;
});

function updateValue() {
  emit("updateValue", inputValue.value);
  nextTick(() => {
    inputValue.value = numberValue.value;
  });
}
</script>

<template>
  <NumberInput
    @updateValue="updateValue"
    v-model="inputValue"
    :name="name"
    :placeholder="placeholder"
    :required="required"
  />
</template>
