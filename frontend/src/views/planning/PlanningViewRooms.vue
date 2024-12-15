<script setup lang="ts">
import NumberInput from "@/components/NumberInput.vue";
import NumberInputDynamic from "@/components/NumberInputDynamic.vue";
import PrimaryButton from "@/components/PrimaryButton.vue";
import SelectList from "@/components/SelectList.vue";
import SelectListDynamic from "@/components/SelectListDynamic.vue";
import TableCard, { type Ordering } from "@/components/TableCard.vue";
import type { Class, Room } from "@/types";
import { XMarkIcon } from "@heroicons/vue/24/outline";
import axios from "axios";
import { computed, onMounted, ref, toRefs, watch } from "vue";

const props = defineProps<{
  classes: Class[];
}>();

const { classes } = toRefs(props);
const classDescriptions = computed(() =>
  classes.value.map((x) => x.class_description),
);

const rooms = defineModel<Room[]>();

const roomsOrdering = ref<Ordering>();
watch(roomsOrdering, () => {
  fetchRooms();
});

async function fetchRooms() {
  let orderingParam = roomsOrdering.value?.name;
  if (roomsOrdering.value?.order === "descending") {
    orderingParam = `-${orderingParam}`;
  }

  rooms.value = (
    await axios.get("/api/room/", {
      params: {
        ordering: orderingParam,
      },
    })
  ).data;
}

async function changeRoomNumber(roomItem: Room, newNumber: number) {
  if (roomItem.room_number !== newNumber) {
    await axios.patch(`/api/room/${roomItem.id}/`, {
      room_number: newNumber,
    });
    await fetchRooms();
  }
}

async function changeRoomClass(roomItem: Room, newClass: number) {
  if (roomItem.room_class !== newClass) {
    await axios.patch(`/api/room/${roomItem.id}/`, {
      room_class: newClass,
    });
    await fetchRooms();
  }
}

async function changeRoomPlaces(roomItem: Room, newPlaces: number) {
  if (roomItem.places !== newPlaces) {
    await axios.patch(`/api/room/${roomItem.id}/`, {
      places: newPlaces,
    });
    await fetchRooms();
  }
}

async function deleteRoom(roomItem: Room) {
  await axios.delete(`/api/room/${roomItem.id}/`);
  await fetchRooms();
}

const newRoomNumber = ref<number>();
const newRoomPlaces = ref(1);
const newRoomClass = ref<number>();

async function createRoom(): Promise<boolean> {
  if (newRoomNumber.value === undefined || newRoomClass.value === undefined) {
    return false;
  }

  await axios.post("/api/room/", {
    room_number: newRoomNumber.value,
    room_class: classes.value[newRoomClass.value].id,
    places: newRoomPlaces.value,
  });
  await fetchRooms();

  newRoomNumber.value = undefined;
  newRoomPlaces.value = 1;
  newRoomClass.value = undefined;

  return true;
}

onMounted(async () => {
  await fetchRooms();
});
</script>

<template>
  <h1 class="pb-2 pt-6 text-center text-4xl font-extrabold lg:text-start">
    Rooms
  </h1>
  <TableCard
    v-model:ordering="roomsOrdering"
    :columns="[
      { name: 'delete', display: '' },
      { name: 'room_number', display: 'Room number', ordering: true },
      { name: 'places', display: 'Places', ordering: true },
      { name: 'class', display: 'Class' },
      { name: 'submit', display: '' },
    ]"
    :rows="rooms"
    :extraFormRow="{ formName: 'createRoomForm', formSubmit: createRoom }"
  >
    <template #delete="item">
      <button
        class="rounded-md bg-red-500 p-[4px]"
        v-if="!item.isFormRow"
        @click="deleteRoom(item.data)"
      >
        <XMarkIcon class="h-[24px] w-[24px] text-white" />
      </button>
    </template>

    <template #room_number="item">
      <div v-if="!item.isFormRow" class="inline-block w-[100px] lg:w-[150px]">
        <NumberInputDynamic
          :numberValue="item.data.room_number"
          :min="1"
          @updateValue="(value) => changeRoomNumber(item.data, value)"
        />
      </div>
      <div v-else class="inline-block w-[100px] lg:w-[150px]">
        <NumberInput v-model="newRoomNumber" :min="1" />
      </div>
    </template>

    <template #places="item">
      <div v-if="!item.isFormRow" class="inline-block w-[100px] lg:w-[150px]">
        <NumberInputDynamic
          :numberValue="item.data.places"
          @updateValue="(value) => changeRoomPlaces(item.data, value)"
        />
      </div>
      <div v-else class="inline-block w-[100px] lg:w-[150px]">
        <NumberInput v-model="newRoomPlaces" :min="1" :max="10" />
      </div>
    </template>

    <template #class="item">
      <SelectListDynamic
        v-if="!item.isFormRow"
        :options="classDescriptions"
        :selected="classes.findIndex((x) => x.id == item.data.room_class)"
        @updateSelection="
          (value) => changeRoomClass(item.data, classes[value].id)
        "
      />
      <SelectList
        v-else
        :options="classDescriptions"
        v-model="newRoomClass"
        form="createRoomForm"
      />
    </template>

    <template #submit="item">
      <PrimaryButton v-if="item.isFormRow" form="createRoomForm" type="submit"
        >Create new room</PrimaryButton
      >
    </template>
  </TableCard>
</template>
