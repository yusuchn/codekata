/*
=============
OpenCL Kernels
=============

Functions of setting up OpenCL kernel and generating OpenCL functions for image analysis.
*/

// Python.h has to be added before any standard heasders
#include <Python.h>


static PyObject *SpamError; // for defining a new exception of your own
static PyObject *
spam_system(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = system(command);
    return Py_BuildValue("i", sts);

}


static PyMethodDef SpamMethods[] = {
    //add some code ...
    {"system",  spam_system, METH_VARARGS,
     "Execute a shell command."},
    //add somw code ...
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


// our module's initialixation function
PyMODINIT_FUNC
initspam(void)
{
    PyObject *m;

    m = Py_InitModule("spam", SpamMethods);
    if (m == NULL)
        return;

    // defining a new exception of your own
    // normally use pre-defined PyErr_*s'
    // ref. section 1.2 - https://docs.python.org/2/extending/extending.html
    SpamError = PyErr_NewException("spam.error", NULL, NULL);
    Py_INCREF(SpamError);
    PyModule_AddObject(m, "error", SpamError);
}


/*
// alternative C function that will be called when the
// Python expression spam.system(string) is evaluated,
// this one uses our own exception, i.e. SpamError
static PyObject *
spam_system(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;

    // Note, when using PyArg_ParseTuple, the Python-level
    // patameters to be passed in must be a tuple acceptable
    // for passing via PyArg_ParseTuple, in this case, use
    // METH_VARARGS flag when listing its name and address
    // in a "method table".
    // Should the keyword argument to be
    // passed in, our C function should accept a third
    // PyObjbect * parameter, which will be a dictionary
    // of keywords, and we should use  PyArg_ParseTupleAndKeywords()
    // to parse the arguments, and when listing its name and
    // address in the "method table". the flag
    // METH_VARARGS | METH_KEYWORDS should be used
    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = system(command);
    if (sts < 0) {
        PyErr_SetString(SpamError, "System command failed");
        return NULL;
    }
    // return PyLong_FromLong(sts);

    // for now we use the original C function (ref. above), ie.
    // return an python integer object,
    // note, Our spam.system() function must return the value of
    // sts as a Python object, integer i is build into python
    // object using Py_BuildValue
    // note also, if the c function intending return nothing, ie.
    // void, the corresponding Pyton function must return None.
    // for example:
    //Py_INCREF(Py_None);
    //return Py_None;
    // note, Py_None is the C name for the special Python object None.
    // It is a genuine Python object rather than a NULL pointer,
    // which means “error” in most contexts, as we have seen.
    return Py_BuildValue("i", sts);
}
*/


/*
Py_INCREF(Py_None);
return Py_None;
*/



int
main(int argc, char *argv[])
{
    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(argv[0]);

    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();

    /* Add a static module */
    initspam();

    // ...
}


