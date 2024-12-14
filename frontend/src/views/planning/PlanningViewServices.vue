<script setup lang="ts">
import EditableLabel from "@/components/EditableLabel.vue";
import PrimaryButton from "@/components/PrimaryButton.vue";
import SelectMulti from "@/components/SelectMulti.vue";
import SelectMultiDynamic from "@/components/SelectMultiDynamic.vue";
import TableCard, { type Ordering } from "@/components/TableCard.vue";
import TextField from "@/components/TextField.vue";
import type { Class, Service } from "@/types";
import { XMarkIcon } from "@heroicons/vue/24/outline";
import axios from "axios";
import { computed, onMounted, ref, toRefs, watch } from "vue";

const CURRENCY_SYMBOL = import.meta.env.VITE_CURRENCY_SYMBOL;

const props = defineProps<{
  classes: Class[];
}>();

const { classes } = toRefs(props);
const classDescriptions = computed(() =>
  classes.value.map((x) => x.class_description),
);

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

onMounted(async () => {
  await fetchServices();
});
</script>

<template>
  <h1 class="pb-2 pt-6 text-center text-4xl font-extrabold lg:text-start">
    Services
  </h1>
  <TableCard
    v-model:ordering="servcesOrdering"
    :columns="[
      { name: 'delete', display: '' },
      {
        name: 'service_description',
        display: 'Service description',
        ordering: true,
      },
      { name: 'service_price', display: 'Service price', ordering: true },
      { name: 'classes', display: 'Classes' },
      { name: 'submit', display: '' },
    ]"
    :rows="services"
    :extraFormRow="{ formName: 'createServiceForm', formSubmit: createService }"
  >
    <template #delete="item">
      <button
        class="rounded-md bg-red-500 p-[4px]"
        v-if="!item.isFormRow"
        @click="deleteService(item.data)"
      >
        <XMarkIcon class="h-[24px] w-[24px] text-white" />
      </button>
    </template>

    <template #service_description="item">
      <EditableLabel
        v-if="!item.isFormRow"
        class="justify-center"
        :text="item.data.service_description"
        @updateText="(value) => changeServiceDescription(item.data, value)"
      />
      <div v-else class="inline-block w-[100px] lg:w-[250px]">
        <TextField
          placeholder="Service description"
          v-model="newServiceDescription"
          form="createServiceForm"
        />
      </div>
    </template>

    <template #service_price="item">
      <div v-if="!item.isFormRow">
        <EditableLabel
          class="justify-center"
          :text="item.data.service_price.toString()"
          @updateText="(value) => changeServicePrice(item.data, value)"
        />
        {{ CURRENCY_SYMBOL }}
      </div>
      <div v-else class="inline-block w-[100px] lg:w-[250px]">
        <TextField
          placeholder="Service price"
          v-model="newServicePrice"
          form="createServiceForm"
        />
      </div>
    </template>

    <template #classes="item">
      <SelectMultiDynamic
        v-if="!item.isFormRow"
        :options="classDescriptions"
        :selected="
          item.data.classes.map((x) => classes.findIndex((y) => y.id == x))
        "
        placeholder="Select classes"
        @updateSelections="(value) => changeServiceClasses(item.data, value)"
      />
      <SelectMulti
        v-else
        v-model="newServiceClasses"
        :options="classDescriptions"
        placeholder="Select classes"
      />
    </template>

    <template #submit="item">
      <PrimaryButton
        v-if="item.isFormRow"
        form="createServiceForm"
        type="submit"
        >Create new service</PrimaryButton
      >
    </template>
  </TableCard>
</template>
