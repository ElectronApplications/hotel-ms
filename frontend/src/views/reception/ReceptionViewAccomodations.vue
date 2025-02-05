<script setup lang="ts">
import CheckboxDynamic from "@/components/CheckboxDynamic.vue";
import PrimaryButton from "@/components/PrimaryButton.vue";
import SelectList from "@/components/SelectList.vue";
import TableCard from "@/components/TableCard.vue";
import TextField from "@/components/TextField.vue";
import type { Room, Accomodation, Class, Pagination, Client } from "@/types";
import axios from "axios";
import { computed, onMounted, ref, watch } from "vue";
import { useI18n } from "vue-i18n";

const CURRENCY_SYMBOL = import.meta.env.VITE_CURRENCY_SYMBOL;

const { t } = useI18n({
  messages: {
    en: {
      accomodations: "Accomodations",
      roomNumber: "Room number",
      moveInTime: "Move in time",
      moveOutTime: "Move out time",
      client: "Client",
      price: "Price",
      checkedOut: "Checked out",
      paid: "Paid",
      noneFound: "None found",
      createAccomodation: "Create new accomodation",
    },
    ru: {
      accomodations: "Проживание",
      roomNumber: "Номер комнаты",
      moveInTime: "Время въезда",
      moveOutTime: "Время выезда",
      client: "Клиент",
      price: "Стоимость",
      checkedOut: "Выехали",
      paid: "Оплатили",
      noneFound: "Не найдено",
      createAccomodation: "Создать новое проживание",
    },
  },
});

const accomodations = ref<Accomodation[]>([]);

const rooms = ref<Room[]>([]);
const roomNumbers = computed(() =>
  rooms.value.map(
    (x) =>
      `№${x.room_number.toString()}, ${x.places} places, ${classes.value.find((y) => y.id == x.room_class)?.class_description}`,
  ),
);

const classes = ref<Class[]>([]);

async function fetchAccomodations() {
  accomodations.value = (await axios.get("/api/accomodation/")).data;
}

async function changeAccomodationCheckedOut(
  accomodationItem: Accomodation,
  newValue: boolean,
) {
  if (accomodationItem.checked_out !== newValue) {
    await axios.patch(`/api/accomodation/${accomodationItem.id}/`, {
      checked_out: newValue,
    });
    await fetchAccomodations();
  }
}

async function changeAccomodationPricePaid(
  accomodationItem: Accomodation,
  newValue: boolean,
) {
  if (accomodationItem.was_price_paid !== newValue) {
    await axios.patch(`/api/accomodation/${accomodationItem.id}/`, {
      was_price_paid: newValue,
    });
    await fetchAccomodations();
  }
}

const newAccomodationRoom = ref(0);
const newAccomodationMoveIn = ref("");
const newAccomodationMoveOut = ref("");

const newAccomodationClientSearch = ref("");
const newAccomodationClients = ref<Pagination<Client>>();
watch(newAccomodationClientSearch, async (value) => {
  newAccomodationClients.value = (
    await axios.get("/api/client/", {
      params: {
        search: value,
      },
    })
  ).data;
});
const newAccomodationClient = computed(() =>
  newAccomodationClients.value !== undefined &&
    newAccomodationClients.value.count !== 0
    ? newAccomodationClients.value.results[0]
    : undefined,
);

const priceToPay = computed(() => {
  const oneDay = 24 * 60 * 60 * 1000;
  const diff =
    new Date(newAccomodationMoveOut.value).getTime() -
    new Date(newAccomodationMoveIn.value).getTime();
  const days = Math.round(diff / oneDay);

  if (rooms.value.length === 0 || classes.value.length === 0) {
    return undefined;
  }

  return (
    rooms.value[newAccomodationRoom.value].places *
    classes.value.find(
      (x) => x.id == rooms.value[newAccomodationRoom.value].room_class,
    )!.place_price *
    days
  );
});

async function createAccomodation(): Promise<boolean> {
  if (
    priceToPay.value === undefined ||
    isNaN(priceToPay.value) ||
    newAccomodationClient.value === undefined
  ) {
    return false;
  }

  await axios.post("/api/accomodation/", {
    room: rooms.value[newAccomodationRoom.value].id,
    move_in_time: newAccomodationMoveIn.value,
    move_out_time: newAccomodationMoveOut.value,
    client: newAccomodationClient.value.id,
    price_to_pay: priceToPay.value,
  });

  await fetchAccomodations();
  return true;
}

onMounted(async () => {
  fetchAccomodations();
  rooms.value = (await axios.get("/api/room/")).data;
  classes.value = (await axios.get("/api/class")).data;
});
</script>

<template>
  <h1 class="pt-6 text-center text-4xl font-extrabold lg:text-start">
    Accomodations
  </h1>
  <TableCard :columns="[
    { name: 'room__room_number', display: t('roomNumber') },
    { name: 'move_in_time', display: t('moveInTime') },
    { name: 'move_out_time', display: t('moveOutTime') },
    { name: 'client__phone_number', display: t('client') },
    { name: 'price_to_pay', display: t('price') },
    { name: 'checked_out', display: t('checkedOut') },
    { name: 'was_price_paid', display: t('paid') },
    { name: 'submit', display: '' },
  ]" :rows="accomodations" :extraFormRow="{
      formName: 'createAccomodationForm',
      formSubmit: createAccomodation,
    }">
    <template #room__room_number="item">
      <span v-if="!item.isFormRow">
        {{ item.data.room.room_number }}
      </span>
      <SelectList v-else v-model="newAccomodationRoom" :options="roomNumbers" :defaultOption="0" />
    </template>

    <template #move_in_time="item">
      <span v-if="!item.isFormRow">{{
        new Date(item.data.move_in_time).toUTCString()
        }}</span>
      <input v-else type="datetime-local" v-model="newAccomodationMoveIn" />
    </template>

    <template #move_out_time="item">
      <span v-if="!item.isFormRow">{{
        new Date(item.data.move_out_time).toUTCString()
        }}</span>
      <input v-else type="datetime-local" v-model="newAccomodationMoveOut" />
    </template>

    <template #client__phone_number="item">
      <span v-if="!item.isFormRow">
        {{ item.data.client.phone_number }}
      </span>
      <div v-else>
        <TextField v-model="newAccomodationClientSearch" />
        {{ newAccomodationClient?.phone_number ?? t("noneFound") }}
      </div>
    </template>

    <template #price_to_pay="item">
      <span v-if="!item.isFormRow">
        {{ item.data.price_to_pay }} {{ CURRENCY_SYMBOL }}
      </span>
      <span v-else-if="newAccomodationRoom !== undefined && rooms.length !== 0">{{ priceToPay }} {{ CURRENCY_SYMBOL
        }}</span>
    </template>

    <template #checked_out="item">
      <CheckboxDynamic v-if="!item.isFormRow" :value="item.data.checked_out"
        @updateValue="(value) => changeAccomodationCheckedOut(item.data, value)" />
    </template>

    <template #was_price_paid="item">
      <CheckboxDynamic v-if="!item.isFormRow" :value="item.data.was_price_paid"
        @updateValue="(value) => changeAccomodationPricePaid(item.data, value)" />
    </template>

    <template #submit="item">
      <PrimaryButton v-if="item.isFormRow" type="submit" form="createAccomodationForm" :enabled="priceToPay !== undefined &&
        !isNaN(priceToPay) &&
        newAccomodationClient !== undefined
        ">{{ t("createAccomodation") }}</PrimaryButton>
    </template>
  </TableCard>
</template>
