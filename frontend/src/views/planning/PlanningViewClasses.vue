<script setup lang="ts">
import { RouterLink } from "vue-router";
import EditableLabel from "@/components/EditableLabel.vue";
import PrimaryButton from "@/components/PrimaryButton.vue";
import SelectListDynamic from "@/components/SelectListDynamic.vue";
import TableCard, { type Ordering } from "@/components/TableCard.vue";
import TextField from "@/components/TextField.vue";
import type { Class, Gallery } from "@/types";
import { XMarkIcon } from "@heroicons/vue/24/outline";
import axios from "axios";
import { computed, onMounted, ref, toRefs, watch } from "vue";
import PlanningViewGalleryDialog from "./PlanningViewGalleryDialog.vue";
import router from "@/router";

const CURRENCY_SYMBOL = import.meta.env.VITE_CURRENCY_SYMBOL;

const props = defineProps<{
  galleries: Gallery[];
}>();

const { galleries } = toRefs(props);
const galleryNames = computed(() => galleries.value.map((x) => x.name));

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

async function changeClassGallery(classItem: Class, newGallery?: number) {
  if (classItem.gallery?.id !== newGallery) {
    await axios.patch(`/api/class/${classItem.id}/`, {
      gallery: newGallery ?? null,
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

const createGalleryClass = ref<Class>();

async function createGallery(gallery: number) {
  await changeClassGallery(createGalleryClass.value!, gallery);
  createGalleryClass.value = undefined;
  router.push(`/gallery/${gallery}`);
}

onMounted(async () => {
  await fetchClasses();
});
</script>

<template>
  <PlanningViewGalleryDialog
    :open="createGalleryClass !== undefined"
    @close="createGalleryClass = undefined"
    @createGallery="(value) => createGallery(value)"
  />

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
      { name: 'gallery', display: 'Gallery' },
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

    <template #gallery="item">
      <div
        v-if="!item.isFormRow"
        class="flex flex-col items-center justify-center space-x-2 lg:flex-row"
      >
        <SelectListDynamic
          :blankOption="true"
          :options="galleryNames"
          :selected="galleries.findIndex((x) => x.id == item.data.gallery?.id)"
          @updateSelection="
            (value) =>
              changeClassGallery(
                item.data,
                value === undefined ? undefined : galleries[value].id,
              )
          "
        />
        <div
          class="text-link-light dark:text-link-dark flex flex-col text-nowrap font-bold underline lg:items-start"
        >
          <RouterLink
            v-if="item.data.gallery !== null"
            :to="`/gallery/${item.data.gallery.id}`"
            >Edit gallery</RouterLink
          >
          <button @click="createGalleryClass = item.data">
            Create new gallery
          </button>
        </div>
      </div>
    </template>

    <template #submit="item">
      <PrimaryButton
        v-if="item.isFormRow"
        form="createClassForm"
        type="submit"
        :enabled="newClassDescription !== '' && newClassPrice !== ''"
        >Create new class</PrimaryButton
      >
    </template>
  </TableCard>
</template>
