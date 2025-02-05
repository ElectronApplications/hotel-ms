<script setup lang="ts">
import EditableLabel from "@/components/EditableLabel.vue";
import PrimaryButton from "@/components/PrimaryButton.vue";
import SelectMulti from "@/components/SelectMulti.vue";
import SelectMultiDynamic from "@/components/SelectMultiDynamic.vue";
import TableCard, { type Ordering } from "@/components/TableCard.vue";
import TextField from "@/components/TextField.vue";
import router from "@/router";
import type { Class, Gallery, Service } from "@/types";
import { XMarkIcon } from "@heroicons/vue/24/outline";
import axios from "axios";
import { computed, onMounted, ref, toRefs, watch } from "vue";
import PlanningViewGalleryDialog from "./PlanningViewGalleryDialog.vue";
import SelectListDynamic from "@/components/SelectListDynamic.vue";
import { useI18n } from "vue-i18n";

const CURRENCY_SYMBOL = import.meta.env.VITE_CURRENCY_SYMBOL;

const { t } = useI18n({
  messages: {
    en: {
      services: "Services",
      serviceDescription: "Service description",
      servicePrice: "Service price",
      classes: "Classes",
      selectClasses: "Select classes",
      gallery: "Gallery",
      createService: "Create new service",
      editGallery: "Edit gallery",
      createGallery: "Create new gallery",
    },
    ru: {
      services: "Услуги",
      serviceDescription: "Описание услуги",
      servicePrice: "Стоимость услуги",
      classes: "Классы",
      selectClasses: "Выбрать классы",
      gallery: "Галерея",
      createService: "Создать новую услугу",
      editGallery: "Редактировать галерею",
      createGallery: "Создать новую галерею",
    },
  },
});

const props = defineProps<{
  classes: Class[];
  galleries: Gallery[];
}>();

const { classes, galleries } = toRefs(props);
const classDescriptions = computed(() =>
  classes.value.map((x) => x.class_description),
);
const galleryNames = computed(() => galleries.value.map((x) => x.name));

const services = defineModel<Service[]>();

const servcesOrdering = ref<Ordering>();
watch(servcesOrdering, () => {
  fetchServices();
});

async function fetchServices() {
  let orderingParam = servcesOrdering.value?.name;
  if (servcesOrdering.value?.order === "descending") {
    orderingParam = `-${orderingParam}`;
  }

  services.value = (
    await axios.get("/api/service/", {
      params: {
        ordering: orderingParam,
      },
    })
  ).data;
}

async function changeServiceDescription(
  serviceItem: Service,
  newDescription: string,
) {
  if (serviceItem.service_description !== newDescription) {
    await axios.patch(`/api/service/${serviceItem.id}/`, {
      service_description: newDescription,
    });
    await fetchServices();
  }
}

async function changeServicePrice(serviceItem: Service, newPrice: string) {
  const price = Number.parseFloat(newPrice);
  if (serviceItem.service_price !== price) {
    await axios.patch(`/api/service/${serviceItem.id}/`, {
      service_price: price,
    });
    await fetchServices();
  }
}

async function changeServiceClasses(
  serviceItem: Service,
  newClasses: number[],
) {
  const serviceClasses = newClasses.map((x) => classes.value[x].id);

  await axios.patch(`/api/service/${serviceItem.id}/`, {
    classes: serviceClasses,
  });
  await fetchServices();
}

async function changeServiceGallery(serviceItem: Service, newGallery?: number) {
  if (serviceItem.gallery?.id !== newGallery) {
    await axios.patch(`/api/service/${serviceItem.id}/`, {
      gallery: newGallery ?? null,
    });
    await fetchServices();
  }
}

async function deleteService(serviceItem: Service) {
  await axios.delete(`/api/service/${serviceItem.id}/`);
  await fetchServices();
}

const newServiceDescription = ref("");
const newServicePrice = ref("");
const newServiceClasses = ref<number[]>([]);

async function createService(): Promise<boolean> {
  if (
    newServiceDescription.value === "" ||
    newServicePrice.value === "" ||
    newServiceClasses.value.length === 0
  ) {
    return false;
  }

  const price = Number.parseFloat(newServicePrice.value);
  const serviceClasses = newServiceClasses.value.map(
    (x) => classes.value[x].id,
  );

  await axios.post("/api/service/", {
    service_description: newServiceDescription.value,
    service_price: price,
    classes: serviceClasses,
  });
  await fetchServices();

  newServiceDescription.value = "";
  newServicePrice.value = "";
  newServiceClasses.value = [];

  return true;
}

const createGalleryService = ref<Service>();

async function createGallery(gallery: number) {
  await changeServiceGallery(createGalleryService.value!, gallery);
  createGalleryService.value = undefined;
  router.push(`/gallery/${gallery}`);
}

onMounted(async () => {
  await fetchServices();
});
</script>

<template>
  <PlanningViewGalleryDialog :open="createGalleryService !== undefined" @close="createGalleryService = undefined"
    @createGallery="(value) => createGallery(value)" />

  <h1 class="pb-2 pt-6 text-center text-4xl font-extrabold lg:text-start">
    {{ t("services") }}
  </h1>
  <TableCard v-model:ordering="servcesOrdering" :columns="[
    { name: 'delete', display: '' },
    {
      name: 'service_description',
      display: t('serviceDescription'),
      ordering: true,
    },
    { name: 'service_price', display: t('servicePrice'), ordering: true },
    { name: 'classes', display: t('classes') },
    { name: 'gallery', display: t('gallery') },
    { name: 'submit', display: '' },
  ]" :rows="services" :extraFormRow="{ formName: 'createServiceForm', formSubmit: createService }">
    <template #delete="item">
      <button v-if="!item.isFormRow" class="rounded-md bg-red-500 p-[4px]" @click="deleteService(item.data)">
        <XMarkIcon class="h-[24px] w-[24px] text-white" />
      </button>
    </template>

    <template #service_description="item">
      <EditableLabel v-if="!item.isFormRow" class="justify-center" :text="item.data.service_description"
        @updateText="(value) => changeServiceDescription(item.data, value)" />
      <div v-else class="inline-block w-[100px] lg:w-[250px]">
        <TextField :placeholder="t('serviceDescription')" v-model="newServiceDescription" form="createServiceForm" />
      </div>
    </template>

    <template #service_price="item">
      <div v-if="!item.isFormRow">
        <EditableLabel class="justify-center" :text="item.data.service_price.toString()"
          @updateText="(value) => changeServicePrice(item.data, value)" />
        {{ CURRENCY_SYMBOL }}
      </div>
      <div v-else class="inline-block w-[100px] lg:w-[250px]">
        <TextField :placeholder="t('servicePrice')" v-model="newServicePrice" form="createServiceForm" />
      </div>
    </template>

    <template #classes="item">
      <SelectMultiDynamic v-if="!item.isFormRow" :options="classDescriptions" :selected="item.data.classes.map((x) => classes.findIndex((y) => y.id == x))
        " :placeholder="t('selectClasses')" @updateSelections="(value) => changeServiceClasses(item.data, value)" />
      <SelectMulti v-else v-model="newServiceClasses" :options="classDescriptions" :placeholder="t('selectClasses')" />
    </template>

    <template #gallery="item">
      <div v-if="!item.isFormRow" class="flex flex-col items-center justify-center space-x-2 lg:flex-row">
        <SelectListDynamic :blankOption="true" :options="galleryNames"
          :selected="galleries.findIndex((x) => x.id == item.data.gallery?.id)" @updateSelection="(value) =>
              changeServiceGallery(
                item.data,
                value === undefined ? undefined : galleries[value].id,
              )
            " />
        <div class="flex flex-col text-nowrap font-bold text-link-light underline lg:items-start dark:text-link-dark">
          <RouterLink v-if="item.data.gallery !== null" :to="`/gallery/${item.data.gallery.id}`">{{ t("editGallery") }}
          </RouterLink>
          <button @click="createGalleryService = item.data">
            {{ t("createGallery") }}
          </button>
        </div>
      </div>
    </template>

    <template #submit="item">
      <PrimaryButton v-if="item.isFormRow" form="createServiceForm" type="submit" :enabled="newServiceDescription !== '' &&
        newServicePrice !== '' &&
        newServiceClasses.length !== 0
        ">{{ t("createService") }}</PrimaryButton>
    </template>
  </TableCard>
</template>
