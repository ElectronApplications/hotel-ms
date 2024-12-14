<script setup lang="ts">
import EditableLabel from "@/components/EditableLabel.vue";
import PrimaryButton from "@/components/PrimaryButton.vue";
import TableCard, { type Ordering } from "@/components/TableCard.vue";
import TextField from "@/components/TextField.vue";
import type { Class } from "@/types";
import { XMarkIcon } from "@heroicons/vue/24/outline";
import axios from "axios";
import { onMounted, ref, watch } from "vue";

const CURRENCY_SYMBOL = import.meta.env.VITE_CURRENCY_SYMBOL;

const classes = defineModel<Class[]>();

const classesOrdering = ref<Ordering>();
watch(classesOrdering, () => {
  fetchClasses();
});

async function fetchClasses() {
  let orderingParam = classesOrdering.value?.name;
  if (classesOrdering.value?.order === "descending") {
    orderingParam = `-${orderingParam}`;
  }

  classes.value = (
    await axios.get("/api/class/", {
      params: {
        ordering: orderingParam,
      },
    })
  ).data;
}

async function changeClassDescription(
  classItem: Class,
  newDescription: string,
) {
  if (classItem.class_description !== newDescription) {
    await axios.patch(`/api/class/${classItem.id}/`, {
      class_description: newDescription,
    });
    await fetchClasses();
  }
}

async function changeClassPrice(classItem: Class, newPrice: string) {
  const price = Number.parseFloat(newPrice);
  if (classItem.place_price !== price) {
    await axios.patch(`/api/class/${classItem.id}/`, {
      place_price: price,
    });
    await fetchClasses();
  }
}

async function deleteClass(classItem: Class) {
  await axios.delete(`/api/class/${classItem.id}/`);
  await fetchClasses();
}

const newClassDescription = ref("");
const newClassPrice = ref("");

async function createClass(): Promise<boolean> {
  if (newClassDescription.value === "" || newClassPrice.value === "") {
    return false;
  }

  const price = Number.parseFloat(newClassPrice.value);

  await axios.post("/api/class/", {
    class_description: newClassDescription.value,
    place_price: price,
  });
  await fetchClasses();

  newClassDescription.value = "";
  newClassPrice.value = "";

  return true;
}

onMounted(async () => {
  await fetchClasses();
});
</script>

<template>
  <h1 class="pb-2 text-center text-4xl font-extrabold lg:text-start">
    Classes
  </h1>
  <TableCard
    v-model:ordering="classesOrdering"
    :columns="[
      { name: 'delete', display: '' },
      {
        name: 'class_description',
        display: 'Class description',
        ordering: true,
      },
      { name: 'place_price', display: 'Place price', ordering: true },
      { name: 'submit', display: '' },
    ]"
    :rows="classes"
    :extraFormRow="{ formName: 'createClassForm', formSubmit: createClass }"
  >
    <template #delete="item">
      <button
        class="rounded-md bg-red-500 p-[4px]"
        v-if="!item.isFormRow"
        @click="deleteClass(item.data)"
      >
        <XMarkIcon class="h-[24px] w-[24px] text-white" />
      </button>
    </template>

    <template #class_description="item">
      <EditableLabel
        v-if="!item.isFormRow"
        class="justify-center"
        :text="item.data.class_description"
        @updateText="(value) => changeClassDescription(item.data, value)"
      />
      <div v-else class="inline-block w-[100px] lg:w-[250px]">
        <TextField
          placeholder="Class description"
          v-model="newClassDescription"
          form="createClassForm"
        />
      </div>
    </template>

    <template #place_price="item">
      <div v-if="!item.isFormRow">
        <EditableLabel
          class="justify-center"
          :text="item.data.place_price.toString()"
          @updateText="(value) => changeClassPrice(item.data, value)"
        />
        {{ CURRENCY_SYMBOL }}
      </div>
      <div v-else class="inline-block w-[100px] lg:w-[250px]">
        <TextField
          placeholder="Place price"
          v-model="newClassPrice"
          form="createClassForm"
        />
      </div>
    </template>

    <template #submit="item">
      <PrimaryButton v-if="item.isFormRow" form="createClassForm" type="submit"
        >Create new class</PrimaryButton
      >
    </template>
  </TableCard>
</template>
