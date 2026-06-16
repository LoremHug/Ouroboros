// Lean compiler output
// Module: Core
// Imports: Init
#include <lean/lean.h>
#if defined(__clang__)
#pragma clang diagnostic ignored "-Wunused-parameter"
#pragma clang diagnostic ignored "-Wunused-label"
#elif defined(__GNUC__) && !defined(__CLANG__)
#pragma GCC diagnostic ignored "-Wunused-parameter"
#pragma GCC diagnostic ignored "-Wunused-label"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"
#endif
#ifdef __cplusplus
extern "C" {
#endif
LEAN_EXPORT lean_object* l_Core_Two_noConfusion___rarg(uint8_t, uint8_t, lean_object*);
LEAN_EXPORT lean_object* l_Core_sectCycle___boxed(lean_object*);
LEAN_EXPORT lean_object* l_Core_Sect_noConfusion___rarg___lambda__1___boxed(lean_object*);
LEAN_EXPORT uint8_t l_Core_twoToBool(uint8_t);
LEAN_EXPORT lean_object* l_Core_Sect_noConfusion(lean_object*);
LEAN_EXPORT lean_object* l_Core_Sect_toCtorIdx(uint8_t);
LEAN_EXPORT uint8_t l_Core_sectCycle(uint8_t);
LEAN_EXPORT lean_object* l_Core_AddCoherence;
LEAN_EXPORT lean_object* l_Core_iterate___rarg___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_Core_Sect_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* l_Core_Two_toCtorIdx(uint8_t);
static lean_object* l_Core_threePeriodSect___closed__1;
LEAN_EXPORT lean_object* l_Core_iterate___rarg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_Core_Triangle_get(lean_object*);
LEAN_EXPORT lean_object* l_Core_Sect_noConfusion___rarg(uint8_t, uint8_t, lean_object*);
static lean_object* l_Core_Sect_noConfusion___rarg___closed__1;
LEAN_EXPORT lean_object* l_Core_threePeriodSect;
LEAN_EXPORT lean_object* l_Core_Triangle_get___rarg(lean_object*, uint8_t);
LEAN_EXPORT lean_object* l_Core_iterate(lean_object*);
LEAN_EXPORT lean_object* l_Core_twoToBool___boxed(lean_object*);
LEAN_EXPORT lean_object* l_Core_TautCoherence;
LEAN_EXPORT lean_object* l_Core_Two_noConfusion___rarg___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_Core_orbitMap(lean_object*);
LEAN_EXPORT lean_object* l_Core_Two_toCtorIdx___boxed(lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_Core_Two_noConfusion(lean_object*);
lean_object* lean_nat_sub(lean_object*, lean_object*);
LEAN_EXPORT uint8_t l_Core_boolToTwo(uint8_t);
LEAN_EXPORT lean_object* l_Core_Sect_noConfusion___rarg___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_Core_Sect_noConfusion___rarg___lambda__1(lean_object*);
LEAN_EXPORT lean_object* l_Core_boolToTwo___boxed(lean_object*);
LEAN_EXPORT lean_object* l_Core_orbitMap___rarg___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_Core_Triangle_get___rarg___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_Core_orbitMap___rarg(lean_object*, lean_object*, uint8_t);
static lean_object* _init_l_Core_AddCoherence() {
_start:
{
return lean_box(0);
}
}
static lean_object* _init_l_Core_TautCoherence() {
_start:
{
return lean_box(0);
}
}
LEAN_EXPORT lean_object* l_Core_iterate___rarg(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; uint8_t x_5; 
x_4 = lean_unsigned_to_nat(0u);
x_5 = lean_nat_dec_eq(x_2, x_4);
if (x_5 == 0)
{
lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; 
x_6 = lean_unsigned_to_nat(1u);
x_7 = lean_nat_sub(x_2, x_6);
lean_inc(x_1);
x_8 = l_Core_iterate___rarg(x_1, x_7, x_3);
lean_dec(x_7);
x_9 = lean_apply_1(x_1, x_8);
return x_9;
}
else
{
lean_dec(x_1);
lean_inc(x_3);
return x_3;
}
}
}
LEAN_EXPORT lean_object* l_Core_iterate(lean_object* x_1) {
_start:
{
lean_object* x_2; 
x_2 = lean_alloc_closure((void*)(l_Core_iterate___rarg___boxed), 3, 0);
return x_2;
}
}
LEAN_EXPORT lean_object* l_Core_iterate___rarg___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = l_Core_iterate___rarg(x_1, x_2, x_3);
lean_dec(x_3);
lean_dec(x_2);
return x_4;
}
}
LEAN_EXPORT lean_object* l_Core_Sect_toCtorIdx(uint8_t x_1) {
_start:
{
switch (x_1) {
case 0:
{
lean_object* x_2; 
x_2 = lean_unsigned_to_nat(0u);
return x_2;
}
case 1:
{
lean_object* x_3; 
x_3 = lean_unsigned_to_nat(1u);
return x_3;
}
default: 
{
lean_object* x_4; 
x_4 = lean_unsigned_to_nat(2u);
return x_4;
}
}
}
}
LEAN_EXPORT lean_object* l_Core_Sect_toCtorIdx___boxed(lean_object* x_1) {
_start:
{
uint8_t x_2; lean_object* x_3; 
x_2 = lean_unbox(x_1);
lean_dec(x_1);
x_3 = l_Core_Sect_toCtorIdx(x_2);
return x_3;
}
}
LEAN_EXPORT lean_object* l_Core_Sect_noConfusion___rarg___lambda__1(lean_object* x_1) {
_start:
{
lean_inc(x_1);
return x_1;
}
}
static lean_object* _init_l_Core_Sect_noConfusion___rarg___closed__1() {
_start:
{
lean_object* x_1; 
x_1 = lean_alloc_closure((void*)(l_Core_Sect_noConfusion___rarg___lambda__1___boxed), 1, 0);
return x_1;
}
}
LEAN_EXPORT lean_object* l_Core_Sect_noConfusion___rarg(uint8_t x_1, uint8_t x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = l_Core_Sect_noConfusion___rarg___closed__1;
return x_4;
}
}
LEAN_EXPORT lean_object* l_Core_Sect_noConfusion(lean_object* x_1) {
_start:
{
lean_object* x_2; 
x_2 = lean_alloc_closure((void*)(l_Core_Sect_noConfusion___rarg___boxed), 3, 0);
return x_2;
}
}
LEAN_EXPORT lean_object* l_Core_Sect_noConfusion___rarg___lambda__1___boxed(lean_object* x_1) {
_start:
{
lean_object* x_2; 
x_2 = l_Core_Sect_noConfusion___rarg___lambda__1(x_1);
lean_dec(x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* l_Core_Sect_noConfusion___rarg___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
uint8_t x_4; uint8_t x_5; lean_object* x_6; 
x_4 = lean_unbox(x_1);
lean_dec(x_1);
x_5 = lean_unbox(x_2);
lean_dec(x_2);
x_6 = l_Core_Sect_noConfusion___rarg(x_4, x_5, x_3);
return x_6;
}
}
LEAN_EXPORT uint8_t l_Core_sectCycle(uint8_t x_1) {
_start:
{
switch (x_1) {
case 0:
{
uint8_t x_2; 
x_2 = 1;
return x_2;
}
case 1:
{
uint8_t x_3; 
x_3 = 2;
return x_3;
}
default: 
{
uint8_t x_4; 
x_4 = 0;
return x_4;
}
}
}
}
LEAN_EXPORT lean_object* l_Core_sectCycle___boxed(lean_object* x_1) {
_start:
{
uint8_t x_2; uint8_t x_3; lean_object* x_4; 
x_2 = lean_unbox(x_1);
lean_dec(x_1);
x_3 = l_Core_sectCycle(x_2);
x_4 = lean_box(x_3);
return x_4;
}
}
static lean_object* _init_l_Core_threePeriodSect___closed__1() {
_start:
{
lean_object* x_1; 
x_1 = lean_alloc_closure((void*)(l_Core_sectCycle___boxed), 1, 0);
return x_1;
}
}
static lean_object* _init_l_Core_threePeriodSect() {
_start:
{
lean_object* x_1; 
x_1 = l_Core_threePeriodSect___closed__1;
return x_1;
}
}
LEAN_EXPORT lean_object* l_Core_orbitMap___rarg(lean_object* x_1, lean_object* x_2, uint8_t x_3) {
_start:
{
switch (x_3) {
case 0:
{
lean_dec(x_1);
return x_2;
}
case 1:
{
lean_object* x_4; 
x_4 = lean_apply_1(x_1, x_2);
return x_4;
}
default: 
{
lean_object* x_5; lean_object* x_6; 
lean_inc(x_1);
x_5 = lean_apply_1(x_1, x_2);
x_6 = lean_apply_1(x_1, x_5);
return x_6;
}
}
}
}
LEAN_EXPORT lean_object* l_Core_orbitMap(lean_object* x_1) {
_start:
{
lean_object* x_2; 
x_2 = lean_alloc_closure((void*)(l_Core_orbitMap___rarg___boxed), 3, 0);
return x_2;
}
}
LEAN_EXPORT lean_object* l_Core_orbitMap___rarg___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
uint8_t x_4; lean_object* x_5; 
x_4 = lean_unbox(x_3);
lean_dec(x_3);
x_5 = l_Core_orbitMap___rarg(x_1, x_2, x_4);
return x_5;
}
}
LEAN_EXPORT lean_object* l_Core_Triangle_get___rarg(lean_object* x_1, uint8_t x_2) {
_start:
{
switch (x_2) {
case 0:
{
lean_object* x_3; 
x_3 = lean_ctor_get(x_1, 0);
lean_inc(x_3);
return x_3;
}
case 1:
{
lean_object* x_4; 
x_4 = lean_ctor_get(x_1, 1);
lean_inc(x_4);
return x_4;
}
default: 
{
lean_object* x_5; 
x_5 = lean_ctor_get(x_1, 2);
lean_inc(x_5);
return x_5;
}
}
}
}
LEAN_EXPORT lean_object* l_Core_Triangle_get(lean_object* x_1) {
_start:
{
lean_object* x_2; 
x_2 = lean_alloc_closure((void*)(l_Core_Triangle_get___rarg___boxed), 2, 0);
return x_2;
}
}
LEAN_EXPORT lean_object* l_Core_Triangle_get___rarg___boxed(lean_object* x_1, lean_object* x_2) {
_start:
{
uint8_t x_3; lean_object* x_4; 
x_3 = lean_unbox(x_2);
lean_dec(x_2);
x_4 = l_Core_Triangle_get___rarg(x_1, x_3);
lean_dec(x_1);
return x_4;
}
}
LEAN_EXPORT lean_object* l_Core_Two_toCtorIdx(uint8_t x_1) {
_start:
{
if (x_1 == 0)
{
lean_object* x_2; 
x_2 = lean_unsigned_to_nat(0u);
return x_2;
}
else
{
lean_object* x_3; 
x_3 = lean_unsigned_to_nat(1u);
return x_3;
}
}
}
LEAN_EXPORT lean_object* l_Core_Two_toCtorIdx___boxed(lean_object* x_1) {
_start:
{
uint8_t x_2; lean_object* x_3; 
x_2 = lean_unbox(x_1);
lean_dec(x_1);
x_3 = l_Core_Two_toCtorIdx(x_2);
return x_3;
}
}
LEAN_EXPORT lean_object* l_Core_Two_noConfusion___rarg(uint8_t x_1, uint8_t x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = l_Core_Sect_noConfusion___rarg___closed__1;
return x_4;
}
}
LEAN_EXPORT lean_object* l_Core_Two_noConfusion(lean_object* x_1) {
_start:
{
lean_object* x_2; 
x_2 = lean_alloc_closure((void*)(l_Core_Two_noConfusion___rarg___boxed), 3, 0);
return x_2;
}
}
LEAN_EXPORT lean_object* l_Core_Two_noConfusion___rarg___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
uint8_t x_4; uint8_t x_5; lean_object* x_6; 
x_4 = lean_unbox(x_1);
lean_dec(x_1);
x_5 = lean_unbox(x_2);
lean_dec(x_2);
x_6 = l_Core_Two_noConfusion___rarg(x_4, x_5, x_3);
return x_6;
}
}
LEAN_EXPORT uint8_t l_Core_boolToTwo(uint8_t x_1) {
_start:
{
if (x_1 == 0)
{
uint8_t x_2; 
x_2 = 0;
return x_2;
}
else
{
uint8_t x_3; 
x_3 = 1;
return x_3;
}
}
}
LEAN_EXPORT lean_object* l_Core_boolToTwo___boxed(lean_object* x_1) {
_start:
{
uint8_t x_2; uint8_t x_3; lean_object* x_4; 
x_2 = lean_unbox(x_1);
lean_dec(x_1);
x_3 = l_Core_boolToTwo(x_2);
x_4 = lean_box(x_3);
return x_4;
}
}
LEAN_EXPORT uint8_t l_Core_twoToBool(uint8_t x_1) {
_start:
{
if (x_1 == 0)
{
uint8_t x_2; 
x_2 = 0;
return x_2;
}
else
{
uint8_t x_3; 
x_3 = 1;
return x_3;
}
}
}
LEAN_EXPORT lean_object* l_Core_twoToBool___boxed(lean_object* x_1) {
_start:
{
uint8_t x_2; uint8_t x_3; lean_object* x_4; 
x_2 = lean_unbox(x_1);
lean_dec(x_1);
x_3 = l_Core_twoToBool(x_2);
x_4 = lean_box(x_3);
return x_4;
}
}
lean_object* initialize_Init(uint8_t builtin, lean_object*);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_Core(uint8_t builtin, lean_object* w) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin, lean_io_mk_world());
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
l_Core_AddCoherence = _init_l_Core_AddCoherence();
l_Core_TautCoherence = _init_l_Core_TautCoherence();
l_Core_Sect_noConfusion___rarg___closed__1 = _init_l_Core_Sect_noConfusion___rarg___closed__1();
lean_mark_persistent(l_Core_Sect_noConfusion___rarg___closed__1);
l_Core_threePeriodSect___closed__1 = _init_l_Core_threePeriodSect___closed__1();
lean_mark_persistent(l_Core_threePeriodSect___closed__1);
l_Core_threePeriodSect = _init_l_Core_threePeriodSect();
lean_mark_persistent(l_Core_threePeriodSect);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
