"""Functions for computing overlap of a basis set."""
from gbasis._moment_int import _compute_multipole_moment_integrals
from gbasis.base_two_symm import BaseTwoIndexSymmetric
from gbasis.contractions import GeneralizedContractionShell
import numpy as np


class Overlap(BaseTwoIndexSymmetric):
    """Class for obtaining the overlap for a set of Gaussian contractions.

    Attributes
    ----------
    _axes_contractions : tuple of tuple of GeneralizedContractionShell
        Sets of contractions associated with each axis of the array.

    Properties
    ----------
    contractions : tuple of GeneralizedContractionShell
        Contractions that are associated with the first and second indices of the array.

    Methods
    -------
    __init__(self, contractions)
        Initialize.
    construct_array_contraction(contractions_one, contractions_two) :
    np.ndarray(M_1, L_cart_1, M_2, L_cart_2)
        Return the overlap associated with a `GeneralizedContractionShell` instance.
        `M_1` is the number of segmented contractions with the same exponents (and angular momentum)
        associated with the first index.
        `L_cart_1` is the number of Cartesian contractions for the given angular momentum associated
        with the first index.
        `M_2` is the number of segmented contractions with the same exponents (and angular momentum)
        associated with the second index.
        `L_cart_2` is the number of Cartesian contractions for the given angular momentum associated
        with the second index.
    construct_array_cartesian(self) : np.ndarray(K_cart, K_cart)
        Return the overlap integrals associated with Cartesian Gaussians.
        `K_cart` is the total number of Cartesian contractions within the instance.
    construct_array_spherical(self) : np.ndarray(K_sph, K_sph)
        Return the overlap integrals associated with spherical Gaussians (atomic orbitals).
        `K_sph` is the total number of spherical contractions within the instance.
    construct_array_mix(self, coord_types, **kwargs) : np.ndarray(K_cont, K_cont)
        Return the overlap integrals associated with the contraction in the given coordinate system.
        `K_cont` is the total number of contractions within the given basis set.
    construct_array_lincomb(self, transform) : np.ndarray(K_orbs, K_orbs)
        Return the overlap integrals associated with the linear combinations of contractions in the
        given coordinate system.
        `K_orbs` is the number of basis functions produced after the linear combinations.

    """

    @staticmethod
    def construct_array_contraction(contractions_one, contractions_two):
        """Return the evaluations of the given contractions at the given coordinates.

        Parameters
        ----------
        contractions_one : GeneralizedContractionShell
            Contracted Cartesian Gaussians (of the same shell) associated with the first index of
            the overlap.
        contractions_two : GeneralizedContractionShell
            Contracted Cartesian Gaussians (of the same shell) associated with the second index of
            the overlap.

        Returns
        -------
        array_contraction : np.ndarray(M_1, L_cart_1, M_2, L_cart_2)
            Overlap associated with the given instances of GeneralizedContractionShell.
            First axis corresponds to the segmented contraction within `contractions_one`. `M_1` is
            the number of segmented contractions with the same exponents (and angular momentum)
            associated with the first index.
            Second axis corresponds to the angular momentum vector of the `contractions_one`.
            `L_cart_1` is the number of Cartesian contractions for the given angular momentum
            associated with the first index.
            Third axis corresponds to the segmented contraction within `contractions_two`. `M_2` is
            the number of segmented contractions with the same exponents (and angular momentum)
            associated with the second index.
            Fourth axis corresponds to the angular momentum vector of the `contractions_two`.
            `L_cart_2` is the number of Cartesian contractions for the given angular momentum
            associated with the second index.

        Raises
        ------
        TypeError
            If contractions_one is not a GeneralizedContractionShell instance.
            If contractions_two is not a GeneralizedContractionShell instance.

        """
        if not isinstance(contractions_one, GeneralizedContractionShell):
            raise TypeError("`contractions_one` must be a GeneralizedContractionShell instance.")
        if not isinstance(contractions_two, GeneralizedContractionShell):
            raise TypeError("`contractions_two` must be a GeneralizedContractionShell instance.")

        coord_a = contractions_one.coord
        angmoms_a = contractions_one.angmom_components_cart
        alphas_a = contractions_one.exps
        coeffs_a = contractions_one.coeffs
        norm_a_prim = contractions_one.norm_prim_cart
        coord_b = contractions_two.coord
        angmoms_b = contractions_two.angmom_components_cart
        alphas_b = contractions_two.exps
        coeffs_b = contractions_two.coeffs
        norm_b_prim = contractions_two.norm_prim_cart
        return _compute_multipole_moment_integrals(
            np.zeros(3),
            np.zeros((1, 3), dtype=int),
            coord_a,
            angmoms_a,
            alphas_a,
            coeffs_a,
            norm_a_prim,
            coord_b,
            angmoms_b,
            alphas_b,
            coeffs_b,
            norm_b_prim,
        )[0]


def overlap_cartesian(basis):
    """Return the overlap of the basis set in the Cartesian form.

    Parameters
    ----------
    basis : list/tuple of GeneralizedContractionShell
        Contracted Cartesian Gaussians (of the same shell) that will be used to construct an array.

    Returns
    -------
    array : np.ndarray(K_cart, K_cart)
        Array associated with the given set of contracted Cartesian Gaussians.
        First and second indices of the array are associated with the contracted Cartesian
        Gaussians. `K_cart` is the total number of Cartesian contractions within the instance.

    """
    return Overlap(basis).construct_array_cartesian()


def overlap_spherical(basis):
    """Return the overlap of the basis set in the spherical form.

    Parameters
    ----------
    basis : list/tuple of GeneralizedContractionShell
        Contracted Cartesian Gaussians (of the same shell) that will be used to construct an array.

    Returns
    -------
    array : np.ndarray(K_sph, K_sph)
        Array associated with the atomic orbitals associated with the given set(s) of contracted
        Cartesian Gaussians.
        First and second indices of the array are associated with two contracted spherical Gaussians
        (atomic orbitals). `K_sph` is the total number of spherical contractions within the
        instance.

    """
    return Overlap(basis).construct_array_spherical()


def overlap_mix(basis, coord_types):
    """Return the overlap of the basis set in the given coordinate systems.

    Parameters
    ----------
    basis : list/tuple of GeneralizedContractionShell
        Contracted Cartesian Gaussians (of the same shell) that will be used to construct an array.
    coord_types : list/tuple of str
        Types of the coordinate system for each GeneralizedContractionShell.
        Each entry must be one of "cartesian" or "spherical".

    Returns
    -------
    array : np.ndarray(K_cont, K_cont)
        Array associated with the contractions in the given coordinate systems.
        First and second indices of the array are associated with two contractions in the given
        coordinate system. `K_cont` is the total number of contractions within the given basis set.

    """
    return Overlap(basis).construct_array_mix(coord_types)


def overlap_lincomb(basis, transform, coord_type="spherical"):
    """Return the overlap of the linear combination of the basis set.

    Parameters
    ----------
    basis : list/tuple of GeneralizedContractionShell
        Contracted Cartesian Gaussians (of the same shell) that will be used to construct an array.
    transform : np.ndarray(K_orbs, K_sph)
        Array associated with the linear combinations of spherical Gaussians (LCAO's).
        Transformation is applied to the left, i.e. the sum is over the second index of `transform`
        and first index of the array for contracted spherical Gaussians.
    coord_type : {"cartesian", list/tuple of "cartesian" or "spherical", "spherical"}
        Types of the coordinate system for the contractions.
        If "cartesian", then all of the contractions are treated as Cartesian contractions.
        If "spherical", then all of the contractions are treated as spherical contractions.
        If list/tuple, then each entry must be a "cartesian" or "spherical" to specify the
        coordinate type of each GeneralizedContractionShell instance.
        Default value is "spherical".

    Returns
    -------
    array : np.ndarray(K_orbs, K_orbs)
        Array whose first and second indices are associated with the linear combinations of the
        contractions.
        First and second indices of the array correspond to the linear combination of contractions.
        `K_orbs` is the number of basis functions produced after the linear combinations.

    """
    return Overlap(basis).construct_array_lincomb(transform, coord_type)
